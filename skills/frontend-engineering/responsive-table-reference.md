
# Reference: Responsive Standalone Table

Это необязательная reference-заметка по задаче responsive standalone table. Она не входит в обязательный набор startup/frontend-правил, но на неё можно ссылаться при работе с reusable таблицами, mobile card mode и shared table shell.

## Когда открывать

Открывать как дополнительный контекст, если задача касается:

- mobile card mode для shared standalone table;
- автоматического mobile rendering поверх TanStack Table;
- рефакторинга reusable table shell в `shared`;
- разбора ошибок после responsive table migration;
- финальной проверки существующих table consumers после изменения shared shell.

## Практические выводы из задачи

### 1. Function-based headers требуют `meta.mobileLabel`

Если колонка использует `header: () => ...`, automatic mobile card renderer не должен падать назад к `column.id` как к пользовательскому label.

Для таких колонок добавлять `meta.mobileLabel`, если таблица должна нормально работать в automatic mobile cards.

### 2. Не дублировать scroll container вокруг shared `Table`

Если project `Table` primitive уже владеет `overflow-x-auto`, не оборачивать shared standalone table body во второй horizontal scroll container без явной и проверенной необходимости.

Иначе появляется nested scroll risk, особенно заметный на mobile и на стыке table body/footer.

### 3. В `<script setup>` использовать `useSlots()`, а не `$slots`

Если логика слотов нужна внутри script-части Vue SFC, использовать `useSlots()`.

`$slots` допустим в template, но не как typed binding внутри `<script setup>`.

### 4. Desktop cell classes нельзя слепо переносить в mobile assumptions

Даже если shared mobile renderer не использует desktop `cellClass` напрямую, внутренние renderers могут всё ещё содержать `whitespace-nowrap`, compact controls, UUID widgets, badges или monospace content.

После изменения shared mobile table нужно отдельно проверять consumers с длинными значениями и плотными controls.

### 5. Representative visual checks нужны не только для shared shell

После изменения shared responsive table полезно отдельно смотреть representative consumers с повышенным риском:

- sessions table;
- broadcasts table;
- telegram broadcast messages table;
- widgets с плотными filters/toolbars.

## Источник

Заметка агрегирует переносимые выводы из реальной responsive-table миграции. Конкретная проектная история и локальные task/error artifacts не являются частью этого универсального reference.
