
# Aiogram Dialog Manual

Reusable справочник по `aiogram-dialog`. Конкретные package paths, DI contracts и state layout определяются проектом.

Использовать вместе с официальной документацией:

- `https://aiogram-dialog.readthedocs.io/en/stable/transitions/`

## Главная модель

`aiogram-dialog` строит Telegram UI из трех основных уровней:

```text
StatesGroup -> Window -> Dialog
```

`StatesGroup` описывает состояния экранов.

`Window` описывает один экран: текст, media, кнопки, getter-ы, message handlers и
состояние, которому этот экран соответствует.

`Dialog` объединяет одно или несколько `Window`.

Пример:

```python
from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, SwitchTo
from aiogram_dialog.widgets.text import Const


class AccountStates(StatesGroup):
    menu = State()
    settings = State()


def create_account_dialog() -> Dialog:
    return Dialog(
        Window(
            Const("Аккаунт"),
            SwitchTo(Const("Настройки"), id="settings", state=AccountStates.settings),
            state=AccountStates.menu,
        ),
        Window(
            Const("Настройки"),
            Back(Const("Назад")),
            state=AccountStates.settings,
        ),
    )
```

## Где держать states

Рекомендуемый layout: dialog-specific `StatesGroup` держать рядом с окнами, которые его используют, если repository structure не задаёт другой owner:

```text
presentation/telegram/_dialogs/_account/_states.py
  class AccountStates(StatesGroup)

presentation/telegram/_dialogs/_account/_dialog.py
  create_account_dialog()
```

Если state не относится к dialog window, а нужен для обычного FSM-flow, держать
его рядом с handlers. Например captcha/banned/MFA states живут в:

```text
presentation/telegram/_handlers.py
```

Не нужно заводить общий `DialogContext`, общий `DialogStates` или глобальный
registry widget id без реальной причины.

## Widget id

`id` у кнопок и stateful widgets нужен для callback data и внутреннего состояния
виджета. Он должен быть стабильной строкой.

Для простых одноразовых кнопок `id` пишется прямо в виджете:

```python
SwitchTo(Const("Настройки"), id="settings", state=AccountStates.settings)
```

Константы нужны только тогда, когда `id` становится локальным контрактом, а не
просто callback id одной кнопки:

- id переиспользуется в нескольких виджетах или функциях;
- id передается в helper/factory;
- id относится к stateful widgets (`Select`, `ScrollingGroup`, `PrevPage`,
  `NextPage`, `CurrentPage`);
- id участвует в формировании других ids;
- это semantic item id/filter id/channel id, который хранится в `dialog_data`,
  `widget_data` или приходит в `on_click`.

В таких случаях ids хранятся локальными константами в модуле окна:

```python
SETTINGS_BUTTON_ID = "settings"
BACK_TO_ACCOUNT_BUTTON_ID = "back_to_account"
```

Не выносить ids в общий enum, если id используется только в одном window module.
Не заводить константу только ради одного `id="..."` рядом с кнопкой.

Для стандартного `Cancel(Const("Назад"))` id обычно не задается: у `Cancel` есть
нормальный дефолтный id.

## Переходы

Основные типы переходов:

- `SwitchTo` — перейти в конкретное окно внутри текущего `Dialog`.
- `Back` — вернуться на предыдущее окно внутри текущего `Dialog`.
- `Start` — открыть другой `Dialog` поверх текущего stack.
- `Cancel` — закрыть текущий `Dialog` и вернуться к предыдущему dialog в stack.

### SwitchTo

`SwitchTo` не меняет dialog stack. Он просто переключает текущее окно внутри
того же dialog context. Данные `dialog_data` и `widget_data` остаются теми же.

```python
SwitchTo(Const("Архив"), id="archive", state=CatalogStates.archive)
```

Использовать для:

- вкладок внутри одного раздела;
- перехода в конкретный экран того же `StatesGroup`;
- кнопки "Назад", если возврат всегда должен вести в конкретный state, а не в
  предыдущее окно по истории.

Пример:

```python
SwitchTo(Const("Назад"), id="back_to_catalog", state=CatalogStates.menu)
```

Не использовать `SwitchTo` для перехода в другой `StatesGroup`. Если целевой
state находится в другом `StatesGroup`, это другой `Dialog` и нужен `Start`.

### Back

`Back` возвращает на предыдущее окно внутри текущего `Dialog`.

```python
Back(Const("Назад"))
```

Использовать для обычной кнопки "Назад" внутри одного dialog, когда пользователь
пришел на экран из предыдущего окна этого же dialog:

```text
ExampleMenuStates.menu
  SwitchTo(ExampleMenuStates.settings)

ExampleMenuStates.settings
  Back("Назад") -> ExampleMenuStates.menu
```

Не использовать `Back`, если экран может открываться из разных мест, а кнопка
должна всегда вести в строго заданный state. В таком случае использовать
`SwitchTo(..., state=...)`.

### Start

Для открытия другого dialog использовать `Start`:

```python
Start(
    Const("Аккаунт"),
    id="account",
    state=AccountStates.menu,
)
```

Обычный `Start` открывает новый dialog поверх текущего в том же stack. Это значит,
что текущий dialog остается под ним, а новый dialog можно закрыть и вернуться
назад.

Использовать `Start` для:

- перехода из главного меню в раздел;
- перехода из родительского меню во вложенное меню с собственным `StatesGroup`;
- запуска самостоятельного сценария, который должен иметь свой `dialog_data`.

Не использовать `Start` для перехода между окнами одного `Dialog`; там нужен
`SwitchTo` или `Back`.

### Cancel

Для закрытия текущего dialog использовать `Cancel`:

```python
Cancel(Const("Назад"))
```

`Cancel` закрывает текущий dialog context. Если он был открыт через `Start`, user
возвращается к предыдущему dialog в stack.

Использовать `Cancel` для кнопки "Назад" на корневом окне дочернего dialog:

```text
AdminPanel dialog
  Start(ReportsMenuStates.menu)

ReportsMenuStates.menu
  Cancel("Назад") -> закрыть ReportsMenuStates и вернуться в AdminPanelStates
```

Не использовать `Cancel` для возврата с дочернего окна на меню внутри того же
dialog. В таком случае `Cancel` закроет весь dialog, а нужен `Back` или
`SwitchTo`.

Типичный паттерн:

```text
MainMenuStates dialog
  Start(AccountStates.menu)

AccountStates dialog
  Cancel("Назад") -> вернуться в MainMenuStates
```

Не делать кнопку "Назад" через жесткий `Start(..., MainMenuStates.menu,
StartMode.RESET_STACK)`, если ожидается возврат по истории.

Краткое правило выбора:

```text
нужно открыть другой StatesGroup/Dialog -> Start
нужно закрыть текущий Dialog -> Cancel
нужно вернуться на предыдущий экран текущего Dialog -> Back
нужно перейти в конкретный state текущего Dialog -> SwitchTo
```

## Вложенные меню как отдельные Dialog

Вложенное меню можно и нужно оформлять отдельным `Dialog`, если оно является
самостоятельным разделом со своим набором окон. Его `StatesGroup` должен жить
рядом с окнами этого меню, а не в общем файле состояний.

Пример структуры:

```text
_dialogs/_admin/_admin.py
  class AdminPanelStates(StatesGroup)
  create_admin_panel_dialog()

_dialogs/_admin/reports/_menu.py
  class ReportsMenuStates(StatesGroup)
  create_reports_dialog()
```

Родительский dialog в таком случае импортирует только публичную точку входа
вложенного меню и открывает его через `Start`:

```python
Start(
    Const("Reports"),
    id="admin_reports",
    state=ReportsMenuStates.menu,
)
```

Оба dialog подключаются в результирующий router из `_dialogs.py`:

```python
def create_admin_panel_router() -> Router:
    router = Router(name="presentation.telegram.admin_panel")
    router.include_routers(
        create_admin_panel_dialog(),
        create_reports_dialog(),
    )
    return router
```

Важное ограничение `aiogram-dialog`: все `Window` внутри одного `Dialog` должны
использовать состояния из одного и того же `StatesGroup`. Поэтому нельзя
собрать один `Dialog` из окон `AdminPanelStates` и `ReportsMenuStates` одновременно.

Если переход идет в другой `StatesGroup`, это другой `Dialog` и нужен `Start`.
Если переход идет между окнами того же `StatesGroup`, это тот же `Dialog` и
можно использовать `SwitchTo`, `Next` или `Back`.

## StartMode

`StartMode.NORMAL` используется по умолчанию. Явно указывать его обычно не нужно.
Он открывает dialog поверх текущего stack.

`StartMode.RESET_STACK` сбрасывает stack и стартует dialog как новый корень.
Использовать только когда пользователь действительно начинает сценарий заново или
нужно восстановиться из битого состояния.

Подходящие места для `RESET_STACK`:

- `/start`;
- успешное завершение captcha, когда нужно открыть главное меню как clean entrypoint;
- global error handler для `UnknownIntent`;
- явный сценарий "начать заново".

Неподходящие места:

- кнопка "Назад";
- переход из главного меню в раздел;
- переход между вложенными окнами раздела.

`StartMode.NEW_STACK` нужен для независимых dialog stacks. Не использовать без отдельного обоснования и explicit stack-lifetime requirement.

## Getters

`getter=` загружает данные для текста и widgets окна.

Пример:

```python
from typing import Any, cast


async def get_profile_data(**kwargs: Any) -> dict[str, str]:
    session = cast(SessionPrincipal, kwargs["session"])
    application_use_cases = cast(ApplicationUseCases, kwargs["application_use_cases"])

    profile_url = await application_use_cases.profile.get_url.execute(
        GetProfileUrlQuery(authenticated_user=session)
    )
    return {"profile_url": profile_url.url}
```

Использование:

```python
Window(
    Format("Profile: {profile_url}"),
    getter=get_profile_data,
    state=ProfileStates.menu,
)
```

Правила проекта:

- getter может вызывать application use case через project-provided typed application facade/use-case bundle;
- `aiogram-dialog` передаёт getter контекст через framework contracts; способ DI и typed extraction должен соответствовать integration contract проекта;
- getter не должен обращаться напрямую к repositories, UoW, SQLAlchemy или
  infrastructure details;
- getter возвращает простой `dict`, который используют `Format`, `Select`,
  `ScrollingGroup` и другие widgets.

## dialog_data и widget_data

`dialog_data` подходит для локальных данных текущего dialog instance:

```python
dialog_manager.dialog_data["selected_plan"] = plan_code
```

Использовать для временного состояния UI, которое не является бизнес-состоянием
системы.

Не использовать `dialog_data` как замену application use case или persistence.

`widget_data` управляется stateful widgets. Обычно не трогать вручную без
необходимости.

## Select и списки

Для выбора элемента из списка использовать `Select`.

```python
Select(
    Format("{item[title]}"),
    id="notification_setting",
    item_id_getter=lambda item: item["id"],
    items="notification_settings",
    on_click=on_notification_setting_click,
)
```

`items` указывает ключ из getter result.

`item_id_getter` должен возвращать стабильный string id элемента.

`on_click` получает `item_id` и может обновить `dialog_data`, вызвать use case
или переключить окно.

## Регистрация Dialog

Все dialogs подключаются к dispatcher через `_dialogs.py`:

```python
from aiogram import Router


def create_dialogs_router() -> Router:
    dialogs_router = Router(name="presentation.telegram.dialogs")
    dialogs_router.include_routers(
        create_main_menu_dialog(...),
        create_account_dialog(),
    )
    return dialogs_router
```

В dispatcher:

```python
dp.include_router(create_dialogs_router())
setup_dialogs(dp)
```

`setup_dialogs(dp)` обязателен: он подключает middleware/core handlers
`aiogram-dialog`.

## Handlers и DialogManager

В обычных aiogram handlers `DialogManager` можно получить через DI:

```python
@router.message(CommandStart())
async def start(dialog_manager: DialogManager) -> None:
    await dialog_manager.start(MainMenuStates.menu, mode=StartMode.RESET_STACK)
```

В handlers использовать states напрямую из module, где они объявлены:

```python
from presentation.telegram._dialogs import MainMenuStates
```

Не прокидывать через DI искусственный context только ради доступа к states.

## Практические правила проекта

1. Dialog state объявлять рядом с окнами соответствующего dialog.
2. `StatesGroup` classes называть с суффиксом `States`.
3. Non-dialog FSM state объявлять рядом с handlers.
4. Простые одноразовые widget ids писать inline; локальные константы оставлять
   для переиспользуемых/stateful/semantic ids.
5. Для перехода в конкретный state текущего dialog использовать `SwitchTo`.
6. Для обычного возврата на предыдущее окно текущего dialog использовать `Back`.
7. Для открытия другого dialog использовать `Start` без `RESET_STACK`.
8. Для закрытия текущего dialog и возврата к предыдущему dialog использовать `Cancel`.
9. `RESET_STACK` использовать только для entrypoint/reset/error recovery.
10. Presentation code вызывает application layer только через подготовленные
   services/adapters, не через repositories или UoW.
11. Не добавлять общий context/registry, пока нет реального повторного
   использования или cross-module контракта.
