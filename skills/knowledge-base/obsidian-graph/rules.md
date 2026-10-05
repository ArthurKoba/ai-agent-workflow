
# Obsidian Graph Rules

## Имена узлов

Файл должен быть понятен как самостоятельный узел Graph View.

Не создавать generic-файлы:

- `index.md`;
- `log.md`;
- `discussion.md`;
- `open-discussion.md`;
- `open-questions.md`.

Использовать самодокументирующие имена с владельцем:

- `wiki-index.md`;
- `wiki-log.md`;
- `backend-index.md`;
- `backend-open-questions.md`;
- `frontend-architecture.md`;
- `shared-index.md`.

## Связность

Каждый wiki-файл должен быть связан хотя бы с одним владельцем:

- root/wiki файлы — из `wiki/wiki-index.md`;
- project-файлы — из `<project>-index.md`;
- shared-файлы — из `wiki/shared/shared-index.md`;
- meta-файлы — из `wiki/wiki-index.md` или соответствующего meta-index.

Если на Graph View виден orphan-узел, агент должен найти реальный файл или unresolved link. Реальный файл связать или переименовать. Unresolved link исправить или удалить.

## Graph JSON

Если репозиторий версионирует canonical `graph.json` reference, держать один owner-path и ссылаться на него из остальных страниц вместо копирования полного JSON.

Не хранить несколько конкурирующих полных `graph.json` в разных местах. Справочные страницы должны ссылаться на актуальный JSON, а не копировать его целиком.

## Цветовые группы

Цветовые группы должны отражать смысловые зоны:

- AI Rules root и профильные правила;
- skills;
- wiki/meta;
- wiki/shared;
- project-specific groups such as `backend` and `frontend` when those groups exist.

После переименования wiki-файлов обновлять graph queries и проверять, что старые пути больше не упоминаются.

## Связи

- `README.md`
- `checklist.md`
- `examples.md`
