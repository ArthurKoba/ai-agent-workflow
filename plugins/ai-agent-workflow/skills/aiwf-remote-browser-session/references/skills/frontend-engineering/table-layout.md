
# Таблицы во frontend

Эту заметку нужно читать при задачах, которые добавляют, меняют или ревьюят таблицы, гриды, списки с колонками, пагинацию, сортировку, фильтрацию, выбор строк, видимость колонок, виртуализацию строк или интеграцию TanStack Table во Vue.

## Когда подключать правило

Подключать вместе с `vue-typescript.md` и `ui-layout.md`, если задача касается:

- табличной вёрстки или компонента `Table`;
- TanStack Table, `@tanstack/vue-table`, column definitions, row models или table state;
- pagination, sorting, filtering, column visibility, row selection, expanding, grouping, pinning или virtualized rows;
- серверной пагинации, серверной сортировки или серверных фильтров, связанных с таблицей;
- UX таблиц: empty/loading/error states, toolbar, bulk actions, dense layout, sticky header, horizontal scroll.


Если задача касается reusable table shell/entity wrapper/slots/mobile mode/FSD-размещения, дополнительно читать `standalone-table.md`.

## Актуальная документация TanStack Table

Перед реализацией или ревью нетривиального поведения получать актуальный Vue-specific TanStack Table contract через официальный docs surface, доступный в текущем проекте/tooling. Если доступен официальный TanStack CLI, его можно использовать как детерминированный источник.

Базовая команда для Vue Table:

```bash
npx @tanstack/cli search-docs "pagination sorting filtering" --library table --framework vue --json
```

Правила использования CLI:

- Использовать `search-docs` для поиска релевантных страниц перед тем, как писать или менять логику TanStack Table.
- Всегда передавать `--library table` для задач по TanStack Table.
- Для Vue передавать `--framework vue`; не переносить React-примеры без проверки Vue-документации.
- Всегда добавлять `--json`, чтобы результат можно было разобрать детерминированно.
- Делать запрос точным по функции, которую меняешь: например `"vue table pagination"`, `"column filtering"`, `"row selection"`, `"manual pagination"`, `"column visibility"`, `"sorting state"`, `"virtualized rows"`.
- Если `search-docs` возвращает конкретный путь документации и нужен полный текст страницы, использовать `tanstack doc <library> <path> --json` / `npx @tanstack/cli doc table <path> --json`.
- Если актуальный API contract получить нельзя, не выдумывать TanStack API по памяти; продолжать только там, где отсутствие документации не влияет на корректность.

Справочные источники для этого правила:

- https://tanstack.com/cli/latest/docs/cli-reference
- https://tanstack.com/cli/latest/docs/mcp-migration

## Принципы реализации таблиц

- Headless-логику таблицы держать отдельно от визуальной оболочки: TanStack Table отвечает за состояние и row models, UI-компоненты проекта отвечают за разметку.
- Не смешивать server state и table state без явного контракта: pagination/sorting/filtering должны быть либо client-side, либо manual/server-side с понятной синхронизацией.
- Для серверных таблиц явно задавать manual pagination/sorting/filtering и не включать client row model, который противоречит серверной модели данных.
- Колонки описывать типизированно; accessor keys, cell renderers и meta должны соответствовать типу строки.
- Не хранить сложную бизнес-логику форматирования прямо в template ячейки; выносить повторяемые форматтеры или cell-компоненты.
- Для действий в строке использовать существующие кнопки, dropdown/menu и иконки проекта.
- Для bulk actions показывать состояние выбора строк явно и не прятать опасные действия без подтверждения, если действие разрушительное.


## Standalone table и FSD

Для общей таблицы использовать уже принятый проектом термин/path. Если стандарта нет, `standalone table` / `shared/ui/standalone-table` — понятный neutral default, но не обязательное имя.

Разделять три уровня ответственности:

- standalone table в `shared` — generic shell без домена: table mechanics, slots, pagination, column visibility, loading/empty/error states и responsive layout;
- entity table в `entities/<entity>` — доменное отображение сущности: базовые колонки, labels, neutral filters, formatters, status/avatar/mobile card;
- context composition в `widgets` или `pages` — toolbar, actions, сценарные колонки, query/page state, route context и сборка конкретного блока.

Действия пользователя, подтверждения, API-команды и сценарные состояния размещать в `features`, а в таблицу подключать через slots, action column или composition верхнего слоя.

Подробный порядок проектирования и чеклист хранит `standalone-table.md`. Эта заметка остаётся владельцем обязательных frontend/table правил, а скилл описывает повторяемый workflow разработки и ревью.

## Вёрстка и UX таблиц

- Использовать существующий `Table`/shadcn-vue table-компонент, если он есть в проекте.
- Таблица должна иметь явные состояния loading, error и empty, если данные приходят асинхронно.
- Header, toolbar, filters, table body и pagination должны быть визуально связаны, но не вложены в лишние карточки.
- Для широких таблиц использовать горизонтальный scroll-контейнер, не сжимать колонки до нечитаемого состояния.
- Числа, даты, статусы и действия выравнивать стабильно по колонкам; actions обычно держать в последней колонке с фиксированной шириной.
- Длинный текст в ячейках должен переноситься, обрезаться через `truncate` с доступом к полному значению, либо занимать колонку, рассчитанную на длинный контент.
- Pagination controls должны показывать текущее состояние и disabled-состояния, когда переход невозможен.
- Sorting и filtering controls должны быть доступны с клавиатуры и не ломать layout на мобильном viewport.
- На мобильных экранах выбирать один из устойчивых паттернов: горизонтальный scroll таблицы, сокращённый набор колонок или отдельный responsive row layout. Не допускать наложения текста и controls.

## Проверка перед завершением

- Актуальная документация TanStack Table получена через CLI для нетривиальных изменений API/поведения.
- Использован Vue-specific API, а не непроверенный React-паттерн.
- Таблица типизирована по модели строки.
- Pagination/sorting/filtering согласованы с client-side или server-side моделью данных.
- Loading/error/empty states предусмотрены, если данные асинхронные.
- Layout выдерживает длинные значения, много колонок и мобильный viewport.
- Запущены релевантные проверки проекта: type-check/lint или более узкая команда.

## Необязательный reference по responsive standalone table

Если задача касается automatic mobile cards или разбора ошибок после responsive table refactor, можно дополнительно открыть `responsive-table-reference.md`.
