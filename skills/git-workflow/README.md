
# Правила оформления коммитов

Это reusable default для репозиториев без более строгого локального commit contract. Repository contribution rules и release/history policy имеют приоритет.

Эти правила подключаются перед созданием коммита, изменением сообщения коммита или рекомендацией имени коммита.

Использовать Conventional Commits с понятным телом сообщения, если одного заголовка недостаточно.

## Формат

Базовый формат для обычного коммита:

```text
<type>[optional scope]: <short imperative summary>

<body with the main changes and important context>

[optional footer]
```

Между header и body обязательно должен быть один пустой ряд, то есть в `git commit -m` это отдельный второй `-m` или
сообщение из файла с двойным переносом строки после заголовка.

Однострочный коммит без body допустим только для совсем механических изменений: форматирование, typo, bump версии,
правка одного очевидного комментария или другой тривиальный diff.

Пример обычного коммита:

```text
refactor(user): move user persistence models

Move user creation data into the domain layer and expose the SQLAlchemy
model as UserDB. Replace the public repository module with a private
implementation module exported through repositories.__init__.
```

Примеры коротких header-only коммитов для тривиальных изменений:

```text
style: format imports
docs: fix README typo
```

## Заголовок

- Заголовок обязателен.
- Начинать с типа: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `style`, `build`, `ci`, `chore`, `revert`.
- Scope опционален и пишется в скобках, если он реально помогает: `fix(db): ...`, `feat(bot): ...`.
- После типа или scope ставить двоеточие и пробел.
- Описание писать коротко, конкретно и в повелительном наклонении на английском: `add`, `fix`, `move`, `split`,
  `remove`, `rename`.
- Не писать точку в конце заголовка.
- Не использовать заглушки вроде `todo`, `update`, `fix`, `changes`, `wip`, если они не объясняют изменение.
- Держать заголовок примерно до 50-72 символов; если нужно больше контекста, переносить детали в body.

## Типы

- `feat`: новая пользовательская или бизнес-возможность.
- `fix`: исправление дефекта.
- `refactor`: изменение структуры кода без изменения внешнего поведения.
- `perf`: улучшение производительности.
- `test`: добавление или изменение тестов.
- `docs`: документация и правила без изменения runtime-поведения.
- `style`: форматирование, пробелы, порядок импортов, без изменения логики.
- `build`: зависимости, сборка, packaging.
- `ci`: CI/CD и автоматизация проверок.
- `chore`: техническое обслуживание, не попадающее в другие типы.
- `revert`: откат предыдущего коммита.

Если изменение подходит под несколько типов, выбирать тип по главному пользовательскому или архитектурному эффекту
коммита.

## Body

Body обязателен для любого нетривиального коммита.

- Отделять body от заголовка пустой строкой.
- Писать body по смыслу: основные изменения, зачем они сделаны, важные последствия или ограничения.
- Перечислять все значимые изменения логики приложения, поведения, архитектурных границ, данных, API или инфраструктуры,
  которые важны для понимания коммита.
- Не пересказывать diff построчно и не перечислять каждый файл без необходимости.
- Механические правки упоминать только если они важны для понимания основного изменения.
- Переносить строки body примерно на 72 символах.
- Не добавлять body только для тривиальных механических изменений, где header полностью объясняет diff.

Пример:

```text
refactor(db): move user persistence into repository

Move user persistence behind the repository API and keep SQLAlchemy
models out of handlers. This leaves transaction ownership in services
while repositories only map ORM rows to domain models.
```

## Footer

Footer используется для метаданных:

- breaking changes;
- ссылки на задачи или issue;
- co-authored-by и другие Git trailers.

Breaking change отмечать явно:

```text
feat(api)!: rename order status field

BREAKING CHANGE: API clients must read `status` instead of `state`.
```

## Практика для агента

Перед созданием или изменением коммита агент должен:

1. Посмотреть фактический staged diff коммита.
2. Выбрать type и scope по главному смыслу изменения.
3. Сформулировать заголовок так, чтобы он отвечал на вопрос: "что делает этот коммит?".
4. Для любого нетривиального diff добавить body после пустой строки и описать все значимые изменения логики приложения,
   поведения, архитектурных границ, данных, API или инфраструктуры.
5. Создавать такой коммит через несколько `-m`, например
   `git commit -m "refactor(user): move user persistence models" -m "Move user creation data into the domain layer..."`,
   или через message-файл.
6. Проверить, что сообщение не включает случайные staged-изменения, не относящиеся к коммиту.

Если пользователь просит "нормальный месседж" без деталей, агент сам выбирает header и body по diff и не оставляет
заглушки.

Если пользователь просит "сделай коммит для всех изменений", это по умолчанию означает: staged all relevant current
changes, Conventional Commit header, пустая строка и детальное body со всеми значимыми изменениями логики приложения.

## Источники подхода

- Conventional Commits 1.0.0: `https://www.conventionalcommits.org/en/v1.0.0/`.
- Chris Beams, "How to Write a Git Commit Message": `https://cbea.ms/git-commit/`.
