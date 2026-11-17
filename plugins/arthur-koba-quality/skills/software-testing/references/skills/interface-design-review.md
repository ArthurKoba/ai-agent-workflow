# Interface Design Review and Acceptance

Load this skill when reviewing the usability, information architecture, visual
hierarchy, navigation, accessibility or interaction design of an existing web
application, or preparing its UX acceptance criteria **before** refactoring.
It covers *assessment and evidence*, not automatically redesigning or editing
an interface. Use `frontend-engineering/ui-layout.md` for subsequent UI
implementation, `frontend-engineering/table-layout.md` for table mechanics, and
`code-review.md` for independent source-code review.

## Outcome and authority

Review an interface against **real user tasks**, not just whether it looks
modern or whether components and unit tests exist. Produce a prioritized,
reproducible, route-by-route acceptance backlog using the owning project's
existing issue/decision authority. Keep proposed UI patterns separate from
confirmed product decisions. Do not create a competing issue or planning file.

The user/product owner owns intent, terminology, workflows and trade-offs;
product data contracts and the existing design system constrain solutions.
Where requirements conflict, record the contradiction and decision owner.
A positive lint/build/unit-test result is *not* evidence of browser usability.
Do not start redesign, delete data, reset a browser, publish code, or check off
acceptance tasks merely because a defect seems easy to fix.

## 1. Establish a review contract

1. Recover repository/map and the current task authority. Record the exact
   application build/environment, accessible role, supported browser, data
   provenance, current issue and scope. Separate uncommitted local experiments
   from what is deployed and visible; never confuse the two.
2. Identify the top user jobs (find a record, compare values, edit an order,
   return to a report, sync data, use offline mode, etc.) and their acceptable
   completion paths. Capture the owner's vocabulary and success criterion.
3. Inventory routes, deep links, detail views, cross-record links, overlays,
   tab groups, desktop/mobile variants and critical async states. Build the
   route **and transition** matrix before declaring coverage; checking only
   the landing page or code paths is insufficient.
4. Select comparison baselines: approved design system, adjacent working
   screens, legacy behavior where still applicable, and explicit owner feedback.
   A reference screenshot informs, but never overrides a user flow or contract.
5. Check the relevant browser-session/permissions skill first. Reuse permitted
   tabs and a stable session. Protect actual orders, local data and tokens; avoid
   destructive verification without a separately approved test fixture.

## 2. Evidence model: never collapse these states

Label each finding with a source and its validation level:

- **OWNER REQUIREMENT**: behavior specifically requested; not automatically
  reproduced or implemented.
- **BROWSER OBSERVED**: symptom on a named route, build and viewport; include
  minimal reproducible steps and measured evidence.
- **SOURCE INFERRED**: code suggests a problem; browser outcome still unknown.
- **HYPOTHESIS / DEPENDENCY**: cause, missing data/API contract, or expected
  behavior not yet independently established.

Record environment, width, data size where safe, starting state, actions,
actual/expected result, impact and repeatability. Sanitize console/network
samples; store screenshots/traces only in approved evidence storage. Never
copy real record bodies, secrets, tokens, external project's details or private
browser paths into a public backlog. A browser warning is not proof of its
root cause; distinguish application bug, infrastructure issue, permissions,
network and missing source data.

## 3. Evaluate user-facing meaning before decoration

Review the following dimensions as interdependent flows, not as a checklist of
CSS classes. Document **which** routes fail and **why** the user cannot work.

### Information hierarchy and density

- Show names, descriptions, units, category hierarchy and business values
  before internal IDs. Technical UUIDs/keys belong in secondary disclosure
  (compact label, inspect/copy action), unless the task explicitly needs them.
  If a relationship cannot resolve, show an honest unavailable-data state.
- Reserve space according to information value: an empty card must not occupy
  half a viewport by default. Use meaningful cards, groups and table regions;
  avoid gratuitous wrappers, nested decorative cards and huge unbalanced gaps.
- Clear heading levels, breadcrumb semantics, product/system identity,
  distinct browser title, consistent action naming and language. Dates,
  currency, units, precision and time zones must identify their meaning.
- Compare **the same kind** of entity/action across pages: spacing, columns,
  sort controls, icon use, status colors, statistics, feedback and breakpoints.
  Responsive density may differ without sacrificing data access.

### Navigation and continuity

- Walk list → detail → related record → Back, filtered/paginated list → detail
  → Back, direct URL → detail, browser Forward/Back, refresh and two-tab flows.
  Preserve or deliberately reconstruct filter, sort, page, scroll position,
  expanded rows, draft inputs and costly loaded results where appropriate.
- Long-lived or expensive analytics/editor tables may require opening related
  records in **new tabs** to preserve the original context. Test the user's
  actual contract; do **not** impose `target="_blank"` on every link. Label
  external/new-tab behavior and support keyboard/modifier-click conventions.
- Check sidebar/default preferences versus current-tab state, breadcrumbs,
  route titles, overlays and new-tab initialization. A preference should be
  findable where a user expects it, not mixed into an unrelated navigation
  group.

### Tables, related records and large datasets

- Confirm that a default page size (e.g. 20) is a *page*, not a silent cap.
  Verify full-dataset totals, filtering/sorting semantics, page-size choice,
  pagination, persistent selection and correct labels for linked entities.
- Test dense/wide/nested tables at realistic sizes: horizontal scrolling,
  sticky headers, pinned columns, row-height stability, virtualization,
  truncation/tooltips, touch targeting, and focus after row navigation.
- Prefer comparisons and useful attributes to a list of opaque links. A
  "related offers/stock" panel must answer an actual task with appropriate
  columns, quantities and accessible detail navigation.
- Measure loading and main-thread/DOM cost; don't assume virtualization,
  more loading indicators or more cards solves a slow query or poor hierarchy.

### Stateful and potentially destructive operations

- Distinguish `loading`, `revalidating`, `ready`, `stale`, `failed`, `offline`,
  `partial`, `empty`, `disabled` and `cancelled`. Each state requires truthful
  labels, actionable recovery, and stable geometry.
- Show the **local read time**, **last successful local commit** and **server
  data revision** separately; one does not prove another. Reactive database
  subscriptions are not a server freshness protocol. Do not invent polling,
  server push, automatic updates or download percentage without real support.
- Keep primary safe actions near the affected data. Confirm before dangerous
  operations and explain scope. Never make data deletion an ordinary table
  refresh or erase unrelated documents/diagnostics as a side effect.
- For offline/online controls, test readiness and return path, and clarify
  whether a control is manual preference, actual connectivity or auth status.

### Images and browser-local persistence

- Check `img` display separately from binary `fetch`/OPFS caching. An image
  can render cross-origin while its response is unreadable by JavaScript due
  to CORS. Inspect HTTP status, allowed origin, secure-context capability,
  read/write behavior, offline fallback and reset independently.
- Review both HTTPS deployed and local development routing *against the
  product's approved network contract*. Do not enable or keep a proxy solely
  because it makes a local test pass. Do not call an image-cache issue fixed
  because an on-screen fallback displays a picture.

### Accessibility and adaptability

- Check keyboard, focus visibility/order/return, semantic control names,
  table headings, dialogs, confirmations, announcements, target size,
  contrast, zoom, reduced motion and long/translated strings.
- Help affordances should explain a concrete action or value, not repeat its
  label. Support hover **and** focus; touch users need a workable disclosure.
  A copy action or interactive menu belongs in a popover/dialog, not an
  unfocusable tooltip. Use the project's accessible primitives.
- Check narrow phones, tablet and wide desktop, sidebar open/closed, mobile
  keyboard open and cross-axis scroll. If an element is off-screen, identify
  the owning layout constraint before adjusting shared padding.

## 4. Route/transition acceptance matrix

Each meaningful route *and* critical transition receives an entry. A compact
matrix is preferable to many duplicated screen-by-screen prose reports:

| Route / flow | Environment / viewport | User task | Actual behavior + evidence | Expected behavior | Severity / confidence | Verification remaining |
|---|---|---|---|---|---|---|
| List → detail → Back | desktop, named build | resume a filtered list | observed/source/owner tagged | return with filter, page and scroll intact | P1 / observed | mouse, keyboard, refresh |

Inspect at least: landing/navigation, settings and account, entity lists and
entity details, reports/analytics, data/refresh screens, editable documents,
error/empty/offline states and mobile variants. Record "not tested" rather
than implicitly passing a page that was merely opened. A global component
fix is not accepted until its affected screens are revisited.

For every issue, include: stable short ID, severity, source label, affected
routes, reproduction, user consequence, expected UX, suspected owning layer
(if known), acceptance checks, dependencies and evidence locator. Severity:

- **P0**: blocks a core task, causes data loss, or makes navigation/data
  correctness unsafe.
- **P1**: repeatable high-friction task failure or material misleading UI.
- **P2**: substantial consistency, access or secondary-task issue.
- **P3**: minor polish without task impact.

Keep priority separate from confidence and implementation complexity.

## 5. Review-to-implementation and release gates

1. Deliver a **documentation-only** audit first when requested. Group related
   failures by UX contract and map them to the existing issue/checklist.
   Distinguish approved target design, proposals, and unresolved questions.
2. After the owner accepts the direction, plan cohesive changes by user
   journey and shared component. Do not scatter ad-hoc fixes or ship many
   intermediate commits while the overall UI contract is undecided.
3. Validate locally using the project's actual quality gate, targeted UI
   scenarios and non-destructive fixture data. Review all affected routes at
   desktop and mobile sizes; test slow/failing/offline states and navigation
   recovery. Unit tests and builds are necessary but not sufficient.
4. Verify deployed/dev changes *separately* from local acceptance, including
   cache/Service Worker version, backend and proxy behavior. Publish or mark
   checklist items complete only against explicit acceptance evidence.
5. Summarize verified outcomes, remaining issues, regression risks and the
   exact next decision. An independent reviewer should check high-impact
   design/system changes, but a code-review approval cannot substitute for
   the product owner's UX acceptance.

## Reference standards (apply selectively)

- W3C WCAG 2.2 quick reference: https://www.w3.org/WAI/WCAG22/quickref/
- WAI-ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- WAI-ARIA Tooltip Pattern: https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/
  (work in progress; use as guidance, not an unqualified normative standard)

These accessibility references supplement, not replace, the app's business
workflows, concrete owner decisions or recorded browser evidence.
