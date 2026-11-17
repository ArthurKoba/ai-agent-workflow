# Software Engineering Error Patterns

Confirmed reusable execution failures. Keep project-specific commands and paths in the owning repository, not here.

## Errors

- Project with a lockfile-managed Python environment → run tools through the project runner (for example `uv run`) → imports and dependency versions match the repository. Otherwise: global Python/tool versions may silently differ.
- Restricted/sandboxed `uv` environment cannot access its global cache/interpreter → use an allowed workspace-local cache/interpreter contract → the intended command reaches the project code. Otherwise: setup fails before the actual check.
- Application service calls an external typed port and persistence inside one broad `except Exception` → catch only the declared port failure around the port call → expected adapter failure is translated while persistence/programming defects still surface. Otherwise: an infrastructure defect can be misclassified as a safe business failure.
- Project uses a `src/` layout but a direct ad-hoc Python invocation does not install/configure that layout → use the repository runner/install/PYTHONPATH contract → imports resolve the same way as supported entrypoints. Otherwise: `ModuleNotFoundError` can be mistaken for a source defect.
- Building a synchronous collection from awaitables → await elements explicitly before passing them to a synchronous constructor → values are resolved before collection construction. Otherwise: an async generator/awaitable can reach a synchronous API and fail at runtime.
- Converting one Pydantic model instance to another compatible model → use explicit mapping or `Target.model_validate(source, from_attributes=True)` when attribute-based conversion is intended → validation uses the documented boundary. Otherwise: a foreign model object may be rejected as a non-mapping input.

Promote a new error here only when the failure pattern is reusable across repositories.
