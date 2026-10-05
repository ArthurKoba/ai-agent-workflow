
# Standalone Table Checklist

Перед завершением задачи со standalone-таблицей проверить:

- Подключены релевантные table/UI rules; FSD и examples загружены только если проект использует FSD или задача затрагивает эти границы.
- Generic table shell находится в `shared` и не знает домен, маршруты, роли, статусы сущностей или бизнес-сценарии.
- Имя/path общей таблицы соответствует проектному стандарту; при отсутствии стандарта выбран понятный neutral default.
- Entity table содержит только нейтральное отображение сущности: базовые колонки, labels, filters, форматтеры, mobile card и entity UI.
- Widget/page содержит только композицию контекста: toolbar, actions, query/page state, сценарные колонки, wiring и route/page context.
- Feature-компоненты отвечают за действия пользователя, а не за копию всей таблицы.
- Pagination, column visibility, loading, empty, error и mobile fallback не продублированы в каждом widget.
- Slots спроектированы как стабильные layout-зоны; содержимое приходит сверху, а новый slot добавлен только при новой повторяемой зоне.
- Row actions и bulk actions подключены через feature/widget composition, а не зашиты в entity или shared shell.
- Server-side pagination/sorting/filtering явно отделены от client-side режима и имеют владельца state.
- Mobile view выбран осознанно: horizontal scroll, сокращённый набор колонок или entity mobile card, без наложений и нечитаемых колонок.
- Stable layout проверен для длинных значений, пустого списка, loading/error, disabled pagination, скрытых колонок и узкого viewport.
- Public API не раскрывает лишние внутренние файлы slice и не создаёт deep imports.
- Если нужно менять TanStack Table API или поведение, актуальная Vue-документация получена по правилам table-layout.
