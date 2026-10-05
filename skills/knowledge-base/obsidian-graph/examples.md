
# Obsidian Graph Examples

## Хорошо

- `wiki/wiki-log.md` — понятно, что это журнал wiki.
- `wiki/projects/backend/backend-index.md` — понятно, что это index проекта `backend`.
- `wiki/projects/frontend/frontend-open-questions.md` — понятно, к какому project-space относятся открытые вопросы.
- `wiki/meta/obsidian-graph/obsidian-graph-current-json.md` — понятно, где актуальный Graph JSON.

## Плохо

- `wiki/log.md` — на графе виден голый узел `log`.
- `wiki/projects/backend/index.md` — на графе виден голый узел `index`, непонятно чей.
- `discussion 2` — непонятный orphan-узел без владельца.
- `open question` — непонятно, к какому проекту относится вопрос.

## Исправление

Если есть `discussion 2`, определить владельца. Для cross-project API discussion использовать самодокументирующее имя вроде `shared-api-discussion.md` и связать его из владельца; случайный пустой placeholder удалить.

## Связи

- `README.md`
- `rules.md`
- `checklist.md`
