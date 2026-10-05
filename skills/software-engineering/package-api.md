
# Package API Rules

Использовать при создании/переносе Python packages, изменении публичных импортов и при работе с bounded-context package API. Конкретный layout ниже является reusable паттерном, а не обязательной структурой для каждого Python-репозитория; локальный repository contract имеет приоритет.

## Domain Package Layout

Domain context является публичной границей bounded context. Снаружи domain
context нужно импортировать только из `domain.<context>`.

Базовая структура domain context:

```text
domain/<context>/
  __init__.py
  _entities.py
  _value_objects.py
  _events.py
  _policies.py
  _factories.py
  _services.py
  _errors.py
```

Это список допустимых ролей внутренних файлов, а не обязательный набор для
каждого context. Создавать нужно только те файлы, где уже есть настоящая
доменная роль.

- `_entities.py` — domain entities, aggregate roots и связанные entity-типы.
- `_value_objects.py` — value objects, enums и небольшие domain types.
- `_events.py` — domain events: факты, которые уже произошли в домене.
- `_policies.py` — domain policies, которые принимают domain data и решают
  domain rule без application/infrastructure зависимостей.
- `_factories.py` — domain factories, которые создают domain objects и
  проверяют инварианты создания.
- `_services.py` — domain services без UoW, repositories, outbox, event bus,
  gateway или framework dependencies.
- `_errors.py` — domain-specific invariant/business exceptions.
- `__init__.py` — единственный публичный выход bounded context. Он экспортирует
  только внешний доменный контракт context через явный `__all__`.

Application contracts, ports, UoW, outbox/event bus contracts, worker DTO,
Pydantic command/query/result models и gateway/retry errors не переносятся в
domain. Если policy или service знает про application DTO, auth principal, UoW,
repository, outbox, event bus, worker lifecycle или external gateway behavior,
это не domain object.

## Domain Errors

Domain-specific exceptions живут в `_errors.py` того bounded context, которому
принадлежит инвариант. Если context имеет доменные инварианты, экспортировать
нужно и базовую ошибку context, и публичные конкретные ошибки через
`domain.<context>.__init__`.

Правила:

1. Domain entities, value objects, policies и factories не должны размазывать
   текст ошибок по месту `raise`.
2. Dynamic exception messages собираются внутри classmethod factory на классе
   ошибки.
3. Domain invariants должны выбрасывать domain-specific errors, а не bare
   `ValueError` / `TypeError`.
4. Application boundary validation, Pydantic DTO validation, persistence/JSONB
   parsing errors, gateway errors, worker retry errors и event-bus registry
   errors не переносятся в domain errors.

Пример:

```python
class OrderAlreadyClosedError(DomainOrderError):
    @classmethod
    def for_order(cls, order_uuid: UUID) -> Self:
        msg = f"Order is already closed: {order_uuid}"
        return cls(msg)
```

## Import Rules

1. Снаружи domain context импортировать только из `domain.<context>`.
2. Снаружи domain context не импортировать из `domain.<context>._*.py`.
3. Внутри context импортировать внутренние модули относительно пакета:
   `from ._entities import User`, а не `from domain.user._entities import User`.
4. Поднимать в `__init__.py` только внешний доменный контракт context, не все
   подряд.
5. Cross-context domain imports допустимы только через публичный API другого
   context (`domain.<other_context>`) и только когда это осознанная доменная
   связь, а не способ переиспользовать техническую деталь. Если такая связь
   начинает расти или менять причины изменения context-ов, вынести общий
   vocabulary или пересмотреть границу отдельным архитектурным slice.

## Naming

- Не использовать неоднозначные catch-all модули (`models.py`, `types.py`, `utils.py`) как автоматический стандарт bounded context, если role-specific owner-модули дают более ясную границу.
- Если проект уже имеет стабильный публичный `types`/`models` API, не ломать его механически: оценить ownership и compatibility отдельно.
- SQLAlchemy models остаются в infrastructure/persistence, Pydantic schemas — в presentation/application boundary.
