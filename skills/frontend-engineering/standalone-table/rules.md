
# Standalone Table Rules

## Термины

Standalone table — универсальный table shell без знания бизнес-домена. Он отвечает за механику таблицы, стабильный layout, slots, pagination, column visibility, loading/empty/error states и responsive-поведение.

Entity table — обёртка конкретной сущности. Она знает поля, labels, статусы, базовые колонки, нейтральные filters, форматтеры и mobile card сущности, но не знает сценарий админки, аналитики или конкретной страницы.

Context table composition — widget или page-level сборка, которая соединяет entity table, actions, toolbar, сценарные filters, query/page state и route/page context.

## Общая таблица

Общая standalone table находится в `shared`, если она:

- не содержит доменных типов, статусов, ролей, labels и бизнес-условий;
- принимает данные, columns, controlled/uncontrolled table state и generic options через контракт;
- отдаёт table instance, row/item и state в slots;
- содержит default shell для header, toolbar zones, filters zone, table body, mobile fallback, footer и pagination;
- позволяет заменить содержимое слотов без изменения внутренней структуры shell;
- использует generic i18n только для загрузки, пустого состояния, ошибки, пагинации и настройки колонок.

Следовать принятому в проекте имени/path. Если стандарта нет, `standalone table` / `shared/ui/standalone-table` — нейтральный default, а не обязательное имя.

## Частная таблица

Частная таблица появляется выше `shared`, когда таблица знает смысл данных:

- `entities/<entity>` — базовая таблица сущности, её колонки, neutral filters, mobile card и entity-specific labels;
- `features/*` — таблица только внутри конкретного действия, если таблица полностью подчинена сценарию и не является reusable отображением сущности;
- `widgets/*` — составной блок, который собирает таблицу, toolbar, actions, filters, states и query wiring для области страницы;
- `pages/*` — небольшая уникальная композиция маршрута, если отдельный widget пока не нужен.

Частная таблица не должна копировать standalone shell, pagination, column settings, loading/empty/error или mobile fallback, если эти возможности уже есть в `shared`.

## Slots и точки подмены

Slots нужны для расширения таблицы без размножения shell-компонентов.

Правило ответственности: layout зоны принадлежит standalone table, содержимое зоны передаётся из entity, feature, widget или page.

В standalone table должны быть предусмотрены зоны для:

- title/description или header content;
- toolbar-left и toolbar-right;
- filters;
- row actions или actions column integration;
- custom empty/loading/error states;
- mobile card;
- footer-left;
- pagination override, если стандартная пагинация не подходит.

Slot props должны давать достаточно контекста для подмены, но не протаскивать доменную логику внутрь `shared`: обычно хватает table instance, row, original item, selection state и generic callbacks.

Не добавлять новый slot для каждого частного сценария. Если zone уже существует, расширять содержимое через неё. Новый slot оправдан только когда появляется новая стабильная layout-зона, которую будут использовать повторно.

## Колонки, filters и actions

Базовые колонки сущности принадлежат `entities`, если они описывают поля сущности и могут повторяться в разных блоках.

Сценарные колонки принадлежат `widgets` или `features`, если они добавляют admin/context/page-only данные, row actions или поведение конкретного use case.

Generic filters layout может жить в `shared`, но filters по полям сущности должны быть в `entities`, а сценарные filters — в `features` или композиции `widgets`.

Row actions не должны жить в entity table, если они запускают сценарий. Entity table может предоставить slot или место для actions; сами действия подключаются сверху.

## State и server-side режимы

Standalone table может поддерживать controlled state, но владелец state выбирается по смыслу:

- generic uncontrolled state допустим для локальной column visibility или client-side поведения без persistence;
- state запроса сущности и reusable query params — `entities`;
- state блока, bulk selection и сценарная синхронизация — `widgets`;
- route/query params и navigation — `pages`;
- состояние конкретной команды — `features`.

Для server-side pagination/sorting/filtering table shell должен принимать controlled state и manual flags, а данные считать уже подготовленными верхним слоем. Не смешивать server-side данные с client-side row model, который меняет тот же смысл.

## Mobile и stable layout

Standalone table отвечает за устойчивую механику responsive rendering: desktop table, horizontal scroll или mobile list/card mode по принятому паттерну проекта.

Generic mobile fallback может показывать видимые ячейки как label/value, но важные сущности должны иметь entity mobile card. Context actions добавляются в mobile card сверху через slot или feature/widget composition.

Ширина actions, selection, status, numeric/date columns и controls должна быть стабильной. Длинный текст должен иметь явный режим: wrap, truncate с доступом к полному значению или dedicated wide column.

Loading, empty и error states должны занимать предсказуемую область и не менять каркас таблицы так, чтобы toolbar/footer прыгали между состояниями.

## Public API

Публичный API каждого слоя должен экспортировать только стабильный контракт:

- standalone table и связанные generic contracts из `shared/ui/standalone-table`;
- entity table, базовые columns/factory, entity mobile card и нужные типы из `entities/<entity>`;
- готовую composition из `widgets/<name>`;
- feature actions из соответствующих feature slices.

Внешние consumers не должны импортировать внутренние файлы `ui`, `model`, `api` чужого slice напрямую, если это не локально разрешённый паттерн проекта.
