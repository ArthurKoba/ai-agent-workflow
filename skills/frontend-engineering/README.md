# Frontend Engineering

Use this skill for frontend architecture, Vue/TypeScript applications, Feature-Sliced Design, UI/layout and reusable table work.

## Modules

- Vue 3 / TypeScript application engineering → `vue-typescript.md`
- Feature-Sliced Design → `feature-sliced-design.md`
- FSD placement examples → `feature-sliced-design-examples.md`
- UI/layout and design-system integration → `ui-layout.md`
- table/TanStack Table engineering → `table-layout.md`
- reusable standalone table workflow → `standalone-table.md`
- responsive-table lessons/case-derived reference → `responsive-table-reference.md`

Load only the modules relevant to the current change. A layout-only task does not require all FSD/table documents; an architecture/table refactor normally does.

## Boundaries

- Follow the repository's actual framework, package manager, design system and build scripts.
- Do not introduce a framework/library merely because a module mentions it.
- Project-level frontend architecture and product behavior remain repository/project authority.
- Backend/domain contract changes also require the relevant software-engineering/domain context.

## Completion

Use the project's own type-check, lint, build, browser/runtime and acceptance surfaces as required by the actual risk. Do not impose a universal test/build policy from this skill.
