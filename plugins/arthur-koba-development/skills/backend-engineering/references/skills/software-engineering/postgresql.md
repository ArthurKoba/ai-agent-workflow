
# Оптимизации PostgreSQL в backend-разработке

Это правило подключается для backend-задач, которые касаются PostgreSQL, SQL-запросов, индексов, транзакций, очередей на базе БД, поиска, иерархий, дедупликации, аналитических выборок или производительности database layer.

## Источники

- Habr: [PostgreSQL для бэкендера: 10 фич, которыми мало пользуются, а зря](https://habr.com/ru/companies/netologyru/articles/1051792/).
- PostgreSQL Documentation: [Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html), [SELECT](https://www.postgresql.org/docs/current/sql-select.html), [Window Functions](https://www.postgresql.org/docs/current/tutorial-window.html), [Indexes](https://www.postgresql.org/docs/current/indexes.html), [Full Text Search](https://www.postgresql.org/docs/current/textsearch.html), [Routine Vacuuming](https://www.postgresql.org/docs/current/routine-vacuuming.html).

## Главный принцип

Перед добавлением внешней инфраструктуры, циклов в Python/Go или сложной ручной синхронизации проверить, может ли PostgreSQL решить задачу штатным механизмом: одним SQL-запросом, транзакцией, индексом или встроенной функцией.

Использовать PostgreSQL-возможности не ради «умного SQL», а когда они дают одно из преимуществ:

- атомарность и отсутствие гонок;
- меньше сетевых round-trip между приложением и БД;
- меньше ручной обработки в приложении;
- стабильный и проверяемый план выполнения;
- возможность опереться на индексы;
- упрощение бизнес-кода без потери читаемости.

## Обязательный порядок анализа

1. Сформулировать реальную проблему: медленный запрос, N+1, гонка воркеров, нестабильная дедупликация, лишняя инфраструктура, рост таблицы, блокировки, тяжёлая сортировка или ручная обработка данных в приложении.
2. Проверить, можно ли выразить задачу средствами PostgreSQL без ухудшения читаемости и переносимости, если переносимость важна.
3. Для производительности смотреть `EXPLAIN` или `EXPLAIN ANALYZE`, а не предполагать план выполнения.
4. Для запросов с выбором «первой», «последней» или «лучшей» строки всегда задавать детерминированный `ORDER BY`, включая дополнительный ключ вроде `id`.
5. Для каждого нового индекса объяснить, какой запрос он ускоряет, и проверить цену: размер индекса, замедление записи, пересечение с существующими индексами.
6. Если решение создаёт PostgreSQL-specific SQL, убедиться, что проект не требует совместимости с другой СУБД.

## `FOR UPDATE SKIP LOCKED` для очередей

Применять, когда:

- очередь живёт рядом с данными приложения;
- несколько воркеров должны параллельно забирать задачи без двойной обработки;
- нужна атомарность «забрать и пометить как processing»;
- нагрузка умеренная, а требования не похожи на Kafka/RabbitMQ-level маршрутизацию.

Не применять как замену брокеру, если нужны сложные топики, replay, длительный retention событий, межсервисная доставка, fan-out, delayed routing или независимое масштабирование очереди.

Пример:

```sql
WITH picked AS (
    SELECT id
    FROM jobs
    WHERE status = 'pending'
      AND run_at <= now()
    ORDER BY run_at, id
    LIMIT 10
    FOR UPDATE SKIP LOCKED
)
UPDATE jobs
SET status = 'processing',
    locked_at = now()
WHERE id IN (SELECT id FROM picked)
RETURNING id, payload;
```

Проверки:

- есть индекс под выборку pending-задач, например `(status, run_at, id)` или partial index по `status = 'pending'`;
- есть `locked_at`, retries и механизм возврата зависших `processing`-задач;
- batch size ограничен;
- таблица с частыми `UPDATE`/`DELETE` контролируется через `autovacuum`, очистку старых задач и мониторинг bloat.

### `FOR UPDATE` для защиты `read/check -> write` инвариантов

Использовать обычный `FOR UPDATE` без `SKIP LOCKED`, когда сервис должен последовательно обработать конкурентные изменения одной бизнес-сущности, а не разобрать очередь параллельными воркерами.

Типовая проблема:

```text
T1: SELECT child WHERE owner_id = X -> none
T2: SELECT child WHERE owner_id = X -> none
T1: INSERT child(owner_id = X) -> ok
T2: INSERT child(owner_id = X) -> unique/PK conflict
```

Даже если оба сценария выполняются внутри `session.begin()`, на PostgreSQL `READ COMMITTED` обычная транзакция не блокирует отсутствующую строку и не сериализует проверку `none -> insert`. Она гарантирует атомарность собственных изменений, но не делает предварительное чтение эксклюзивным.

Правильный row-lock сценарий для инварианта, привязанного к существующему owner:

```text
T1: SELECT owner WHERE id = X FOR UPDATE -> lock acquired
T2: SELECT owner WHERE id = X FOR UPDATE -> waits
T1: SELECT child WHERE owner_id = X -> none
T1: INSERT child(owner_id = X)
T1: COMMIT -> lock released
T2: SELECT owner WHERE id = X FOR UPDATE -> continues
T2: SELECT child WHERE owner_id = X -> existing child
T2: returns domain result or raises domain error
```

Что важно:

- `FOR UPDATE` блокирует найденные строки, а не «пустой результат». Поэтому для сценариев создания зависимой записи нужно блокировать уже существующую родительскую/owner-строку: пользователя, заказ или другую существующую родительскую сущность.
- Захватывать lock нужно в начале транзакционного сценария, до проверки зависимых записей и до принятия бизнес-решения.
- Вторая транзакция должна дождаться первой, перечитать зависимое состояние после ожидания и пройти обычную доменную ветку: вернуть существующую связь, отказать в изменении, проверить лимит или создать запись, если инвариант всё ещё позволяет.
- Для такого сценария не использовать `SKIP LOCKED`: он предназначен для очередей и параллельного разбора задач, а не для пользовательских операций, где второй запрос должен увидеть актуальный результат.
- Репозиторий должен иметь явный метод, например `get_by_uuid_for_update`, чтобы call site показывал блокирующее чтение. Не прятать `FOR UPDATE` в обычный `get_by_uuid`, иначе read-only вызовы начнут неожиданно брать locks.
- Метод с `FOR UPDATE` вызывать только внутри транзакционной сессии. Вне транзакции lock будет жить слишком коротко и не защитит последующие проверки и запись.
- Не держать row lock во время внешних запросов, external HTTP/API calls или долгих вычислений. Сценарий должен быть коротким: lock -> read/check -> write -> commit.

Когда выбрать другой механизм:

- `INSERT ... ON CONFLICT` лучше, если конфликт можно атомарно выразить уникальным ограничением и затем доменно обработать результат insert/update.
- `SERIALIZABLE` допустим для широких инвариантов, которые трудно привязать к одной owner-строке, но приложение обязано retry-ить всю транзакцию при serialization failure.
- Advisory lock использовать только когда нет естественной строки данных для блокировки или нужна координация процесса, а не защита конкретной сущности.

Проверки перед завершением:

- есть конкретная owner-строка, которую можно заблокировать;
- lock берётся до проверки зависимых данных;
- все чтения и запись, зависящие от инварианта, находятся в той же транзакции;
- ожидающая транзакция после lock заново читает состояние, а не использует старый результат;
- есть unique/PK constraint как последняя линия защиты целостности;
- код возвращает доменный результат или доменную ошибку, а не полагается на `IntegrityError` как штатную ветку.

## Оконные функции

Применять, когда нужно:

- посчитать значение относительно соседней строки;
- пронумеровать строки внутри группы;
- найти последнюю запись по логическому ключу;
- выполнить дедупликацию;
- посчитать накопительные итоги или агрегаты без выгрузки всех строк в приложение.

Пример интервала между статусами заказа:

```sql
SELECT
    order_id,
    status,
    created_at,
    created_at - lag(created_at) OVER (
        PARTITION BY order_id
        ORDER BY created_at, id
    ) AS time_from_prev_status
FROM order_events
ORDER BY order_id, created_at, id;
```

Пример дедупликации:

```sql
SELECT *
FROM (
    SELECT
        e.*,
        row_number() OVER (
            PARTITION BY order_id, status
            ORDER BY created_at DESC, id DESC
        ) AS rn
    FROM order_events e
) t
WHERE rn = 1;
```

Проверки:

- `ORDER BY` полный и стабильный;
- для больших таблиц проверен план сортировки;
- при необходимости есть индекс под `PARTITION BY` + `ORDER BY`, например `(order_id, created_at, id)`.

## `DISTINCT ON` для первой или последней строки в группе

Применять в PostgreSQL, когда нужна одна строка на группу: последняя сессия пользователя, последний статус заказа, актуальная цена товара, свежий профиль.

Пример:

```sql
SELECT DISTINCT ON (user_id)
    user_id,
    ip,
    user_agent,
    created_at
FROM user_sessions
ORDER BY user_id, created_at DESC, id DESC;
```

Правила:

- `ORDER BY` должен начинаться с выражений из `DISTINCT ON`;
- порядок внутри группы должен быть детерминированным;
- если проект должен быть переносимым между СУБД, предпочесть стандартный вариант через `row_number()`.

## Generated columns

Применять для вычисляемых значений, которые должны храниться согласованно с исходными колонками и не должны синхронизироваться вручную в приложении.

Пример:

```sql
ALTER TABLE users
ADD COLUMN normalized_email text
GENERATED ALWAYS AS (lower(email)) STORED;

CREATE UNIQUE INDEX users_normalized_email_uq
ON users (normalized_email);
```

Когда полезно:

- нормализованные email/phone/search-key;
- вычисляемые суммы или производные поля, если выражение допустимо для generated column;
- индексация результата вычисления без ручного обновления.

Проверки:

- выражение не зависит от нестабильных функций;
- команда миграции учитывает размер таблицы и lock impact;
- generated column не скрывает бизнес-логику, которую лучше оставить в domain/service layer.


## Проверки периодов и дедлайнов

Периодические проверки по timestamp/interval выполнять на стороне PostgreSQL, а не через вычисление deadline в Python.

Правильно:

```python
setup_period_param = bindparam("setup_period", setup_period, type_=Interval())
result = await session.execute(
    select(RecordDB.uuid).where(
        RecordDB.uuid == record_uuid,
        RecordDB.created_at + setup_period_param >= func.now(),
    )
)
```

Нежелательно:

```python
deadline = record.created_at + SETUP_PERIOD
if datetime.now(UTC) > deadline:
    ...
```

Причины:

- единый источник времени — PostgreSQL, а не часы приложения;
- меньше риска timezone drift и расхождения между процессами;
- проверка может быть объединена с выборкой, блокировкой или условным `UPDATE`;
- легче анализировать план запроса и добавить индекс, если проверка становится частой.

Если периодическая проверка является бизнес-инвариантом, сервис должен вызывать понятный метод репозитория, а репозиторий должен выразить сравнение через `func.now()`, `Interval`, `bindparam` или эквивалентный SQLAlchemy/PostgreSQL-механизм.

## `VACUUM`, `autovacuum` и bloat

Учитывать для таблиц с частыми изменениями: очереди, события, сессии, временные статусы, outbox/inbox, soft delete.

Симптомы:

- таблица или индексы растут, хотя данные удаляются;
- запросы постепенно замедляются;
- много `UPDATE` статусов;
- появляются долгие autovacuum-процессы или dead tuples.

Что проверять:

```sql
SELECT
    relname,
    n_live_tup,
    n_dead_tup,
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables
WHERE relname = 'jobs';
```

Правила:

- не считать `DELETE` физическим немедленным уменьшением таблицы;
- для hot-таблиц продумывать retention, batch cleanup, autovacuum-настройки и индексы;
- избегать лишних индексов на таблицах с частыми изменениями.

## `LATERAL JOIN`

Применять, когда для каждой строки внешнего запроса нужен зависимый подзапрос: последние N записей, лучший связанный объект, агрегат по конкретной строке.

Пример: последние 3 события по каждому заказу.

```sql
SELECT
    o.id,
    recent_events.status,
    recent_events.created_at
FROM orders o
LEFT JOIN LATERAL (
    SELECT status, created_at
    FROM order_events e
    WHERE e.order_id = o.id
    ORDER BY created_at DESC, id DESC
    LIMIT 3
) recent_events ON true;
```

Проверки:

- есть индекс под зависимый подзапрос, например `(order_id, created_at DESC, id DESC)`;
- `LATERAL` не превращает запрос в дорогой nested loop на больших выборках без индексов;
- результат понятнее и дешевле, чем отдельные запросы из приложения.

## Recursive CTE

Применять для деревьев и иерархий: категории, меню, организационная структура, вложенные комментарии, parent-child графы ограниченной глубины.

Пример:

```sql
WITH RECURSIVE tree AS (
    SELECT id, parent_id, name, 1 AS depth
    FROM categories
    WHERE id = :root_id

    UNION ALL

    SELECT c.id, c.parent_id, c.name, tree.depth + 1
    FROM categories c
    JOIN tree ON c.parent_id = tree.id
    WHERE tree.depth < 20
)
SELECT *
FROM tree
ORDER BY depth, id;
```

Проверки:

- есть ограничение глубины или защита от циклов;
- есть индекс по `parent_id`;
- для сложных графов оценить, не нужна ли отдельная модель хранения или специализированное решение.

## Advisory locks

Применять для координации backend-процессов, когда нужна блокировка без отдельной таблицы `locks`: singleton cron job, защита от параллельного запуска задачи, координация воркеров.

Пример транзакционной блокировки:

```sql
SELECT pg_try_advisory_xact_lock(hashtext('daily-billing'));
```

Правила:

- использовать `pg_try_advisory_xact_lock`, если блокировка должна жить только до конца транзакции;
- использовать session-level locks только при явной необходимости и аккуратно освобождать;
- ключ блокировки должен быть стабильным и документированным;
- не применять advisory locks вместо нормальных row locks, когда блокируется конкретная строка данных.

## Full-text search

Применять перед добавлением Elasticsearch/OpenSearch, если нужен простой поиск внутри PostgreSQL: статьи, заметки, названия, описания, FAQ, товары без сложного ранжирования и распределённого поиска.

Пример:

```sql
ALTER TABLE articles
ADD COLUMN search_vector tsvector
GENERATED ALWAYS AS (
    to_tsvector('russian', coalesce(title, '') || ' ' || coalesce(body, ''))
) STORED;

CREATE INDEX articles_search_vector_idx
ON articles USING gin (search_vector);

SELECT id, title
FROM articles
WHERE search_vector @@ plainto_tsquery('russian', :query)
ORDER BY ts_rank(search_vector, plainto_tsquery('russian', :query)) DESC;
```

Не применять как замену поисковому движку, если нужны сложные анализаторы, typo tolerance, distributed search, сложное relevance tuning, фасеты с высокой нагрузкой или отдельный search lifecycle.

## Partial indexes

Применять, когда частые запросы обращаются к небольшой и устойчивой части таблицы: активные записи, pending-задачи, не удалённые soft-delete строки, неоплаченные счета.

Пример:

```sql
CREATE INDEX jobs_pending_run_at_idx
ON jobs (run_at, id)
WHERE status = 'pending';
```

```sql
CREATE INDEX users_active_email_idx
ON users (email)
WHERE deleted_at IS NULL;
```

Проверки:

- условие в запросе совпадает с predicate индекса;
- индекс действительно меньше полного и используется планировщиком;
- не создаётся набор частичных индексов на каждый возможный статус без доказанной пользы.

## Когда остановиться и не оптимизировать

Не усложнять SQL и схему, если:

- текущий простой запрос достаточно быстрый и нет измеренной проблемы;
- оптимизация ухудшает читаемость сильнее, чем помогает;
- команда не сможет сопровождать PostgreSQL-specific решение;
- внешняя инфраструктура уже нужна по продуктовым требованиям, а не только из-за одной технической задачи;
- нет теста или проверки, фиксирующей важное поведение оптимизированного запроса.
