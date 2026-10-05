
# Observability Rules

Правила для tracing, logging и будущих metrics.

## Layer Boundaries

1. OpenTelemetry setup, exporters, formatters and instrumentation live in the
   infrastructure/runtime layer.
2. Domain layer must not import OpenTelemetry, logging configuration or runtime
   observability helpers.
3. Application layer must not configure observability. If application code logs,
   use regular named stdlib loggers only; do not configure handlers, exporters or
   global logging state there.
4. Runtime entrypoints/composition roots decide whether observability is enabled
   for the current environment. The observability package must not decide
   `local` / `development` / `production` policy by itself.
5. Use the repository's established logging facade. If no logging contract exists, stdlib `logging` is the conservative default; do not introduce a second logging stack without an explicit reason.

## Tracing

1. Automatic instrumentation is allowed for framework and infrastructure
   boundaries: SQLAlchemy, aiohttp clients, and future FastAPI runtime.
2. Manual spans should be placed at runtime/application orchestration boundaries:
   worker cycle, event delivery handling, notification operation handling,
   broadcast preparation, external gateway operations.
3. Do not add spans inside domain entities, value objects or domain policies.
4. Add span attributes only when they are useful for diagnostics. Avoid dumping
   whole payloads, request bodies or domain objects.
5. Do not put secrets, tokens, passwords, one-time codes, TOTP secrets or payment
   credentials into span names or attributes.
6. Use the observability package helper for manual spans so exceptions are
   recorded consistently and span status is set to error before re-raising.
7. When the aiogram bot runtime is migrated, add presentation/runtime middleware
   that creates a `SpanKind.SERVER` span per incoming Telegram update, records
   safe Telegram attributes such as `telegram.user_id` when useful, and records
   exceptions on the span.

## Logging Levels

Use logs as operational diagnostics, not as a full execution trace.

`INFO`:

- Log broad system actions and lifecycle events.
- Log worker cycle summaries and important state transitions.
- Keep volume low enough for production.

`DEBUG`:

- Log diagnostically useful internal decisions that help investigate bugs.
- Do not log every method entry, repository call or successful micro-step.
- Prefer compact fields that explain why a retry, skip, permanent failure or
  idempotent no-op happened.

`WARNING`:

- Log unexpected but handled conditions.
- Use when the operation can continue, but the situation should be visible.

`ERROR`:

- Log failed operations that require retry, final failure handling or operator
  attention.

Use `logger.exception(...)` only at runtime boundaries where traceback is useful
and the exception is being handled or converted into process-level failure.

## Structured Fields

Prefer structured fields for diagnostics:

```text
worker_name
operation
delivery_uuid
notification_uuid
broadcast_uuid
attempts
max_attempts
next_retry_at
duration_ms
error_type
```

Trace/log correlation is required when tracing is active. Logs emitted inside an
active span should include `trace_id` and `span_id`.

## Trace / Log Correlation

1. Application code should not manually pass `trace_id` or `span_id`.
2. Runtime logging configuration must inject `trace_id` and `span_id`
   automatically from the active OpenTelemetry span.
3. Logs emitted outside an active span may contain null `trace_id` / `span_id`.
4. Do not use `trace_id` or `span_id` as business identifiers, idempotency keys,
   persistence fields or command/query fields.
5. Do not log `trace_id` or `span_id` manually in message text. They belong in
   structured fields controlled by logging infrastructure.
6. During incident investigation, use `trace_id` from a log to find the full
   trace, use trace spans to inspect related SQL/HTTP operations, and use logs
   inside the same trace to understand runtime decisions.

Prefer structured logging with `extra` fields:

```python
logger.info(
    "Notification delivery cycle completed",
    extra={
        "worker_name": worker_name,
        "processed_count": processed_count,
        "retry_count": retry_count,
        "failed_count": failed_count,
    },
)
```

Do not embed correlation fields or structured diagnostics into message text:

```python
logger.info(
    "trace_id=%s processed notification %s",
    trace_id,
    notification_uuid,
)
```

## Payment Logging

Payment and subscription flows may use more detailed logs than generic runtime
flows, but only through dedicated named loggers and structured fields.

Use dedicated logger names:

```python
payment_logger = logging.getLogger("app.payments")
subscription_logger = logging.getLogger("app.subscriptions")
```

Payment logs may include diagnostic fields such as:

```text
payment_uuid
subscription_uuid
provider
operation
provider_payment_id
external_id
amount
currency
status_from
status_to
attempts
max_attempts
provider_status_code
duration_ms
error_type
```

Do not log payment secrets or sensitive payloads:

```text
provider secret keys
signature secrets
raw signatures
Authorization headers
full webhook bodies without redaction
card data
customer-sensitive data beyond what the operation needs for diagnostics
```

Payment logs are diagnostics, not the financial source of truth. Financially
important facts must be stored in domain/application persistence such as payment
ledger, subscription history or audit records. Use logs to investigate runtime
failures, provider calls, idempotency decisions and status transition conflicts.

Detailed payment logging should remain intentional:

- use `INFO` for important payment lifecycle events and final operation results;
- use `DEBUG` for provider-specific decisions needed to diagnose bugs;
- do not log every successful internal micro-step;
- route or tune payment logger level separately when needed, for example through
  a future `PAYMENT_LOG_LEVEL` setting.

## Data Safety

Never log:

```text
Authorization headers
JWTs
passwords
one-time codes
TOTP secrets
raw payment secrets
full request/response bodies from external APIs unless explicitly scrubbed
```

External identifiers may be logged only when they are not credentials or secrets.
Internal identifiers should keep project naming rules: `uuid` / `*_uuid`.
