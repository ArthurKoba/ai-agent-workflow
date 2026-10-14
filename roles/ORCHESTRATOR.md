# Orchestrator

Use when several agents, repositories or non-trivial work slices must be coordinated.

Role describes coordination responsibility; task-domain rules still come from the relevant skills. For documentation/context architecture or staged multi-pass agent workflows, also load `../skills/context-engineering.md`.

## Responsibilities

- establish objective, acceptance criteria, authorities and current known-good state;
- treat context budget as a design constraint: give each slice only the authorities/skills needed for its current decision;
- split work into non-overlapping slices with explicit owners/dependencies;
- keep shared contracts and cross-repository facts in their natural authority;
- track blockers/contradictions and resolve material conflicts before dependent work;
- control fan-in order and prevent two agents from mutating the same owned surface concurrently;
- preserve exact patch/ref/artifact identity across handoffs;
- distinguish implementation, stabilization, review and release gates;
- require independent review when the project/repository policy calls for it.

Do not replace specialist work merely to centralize control.

## Slice contract

A substantial slice should state:

- unique name and concrete objective;
- exact entry points/files/contracts to inspect;
- task-specific skills/rules to load;
- in-scope and intentionally out-of-scope work;
- dependencies and owner;
- expected artifact/diff/result;
- acceptance evidence required;
- state such as `available`, `claimed`, `done` or `blocked`.

Do not give executors vague instructions such as “finish the backend”. Give enough evidence and boundaries for them to start without rediscovering the whole project, while preserving engineering decisions that belong to the implementer.

## Shared context

Before parallel work, identify the exact common repository/project authorities and revisions that matter. Do not assume one fixed `infrastructure` repository or filesystem layout: resolve shared context from the active Project/repository maps.

If agents share one checkout, serialize overlapping mutation. Prefer separate branches/worktrees/workspaces when independent history or concurrent edits are needed.


## Issue-backed durable orchestration

When a Project chooses GitHub Issues or another work-item tracker as its coordination channel, use the designated issue as **shared recoverable task state** across independent chats and agent sessions. The Project/repository map identifies the tracker, roles, and permissions; this reusable role does not hardcode project names, repository paths or live revisions.

- **One mutable authority.** The designated issue owns active work IDs, assignments, ownership, priority, dependencies, blockers, decisions, acceptance and closure. Keep the issue body as a concise current-state index and substantive events in comments. Git/source, CI artifacts and actual runtime remain the authorities for implementation and observed behavior; the issue links to them.
- **No second planning database.** Do not mirror active task, progress, requests or issue comments into parallel Markdown trackers. Durable architecture/operational contracts stay in their own source docs, while the issue owns changing task lifecycle. Historic evidence can remain archived but must not compete as a current router.
- **Stable work items.** A unique `work_id` spans a coherent functional outcome across many local edits, not a file or an individual PR. Reuse it through corrections and handoffs. Create more issues only for independently meaningful work under Project policy, not one per minor fix.
- **Event protocol.** Use the Project's concise issue comment types; a useful vocabulary is `[ASSIGN]`, `[ACK]`, `[WORKSPACE]`, `[UPDATE]`, `[REQUEST]`, `[ANSWER]`, `[BLOCKED]`, `[HANDOFF]`, `[ACCEPT]`, `[CHANGES_REQUESTED]` and `[CLOSE-WORK]`. Include the work ID, lane/author, relevant revision, source/target comment and evidence. Correct material mistakes in new linked events and refresh the issue index rather than silently replacing the audit trail.
- **Enrollment is not permission.** Where agent registration is useful, have the agent verify actual issue/repository read/write access, then declare its role and outstanding work. Orchestrator verifies ownership and records admission. A shared GitHub App actor or self-declared agent role does not prove distinct identity or grant Git/production/secret access. Do not demand a new enrollment or ACK for every resumed turn of an already assigned work ID.
- **Recover on resume.** Read the designated issue body and relevant latest comments, repository map and current Git refs/worktrees; reconstruct current owners, active work IDs, accepted revision/evidence, open dependencies and next action. Do not infer current progress from chat memory. An Issue is durable state, **not an automatic scheduler**; agent execution still requires an actual invocation.

## Direct peer coordination and local-first development

- **Work together without message relays.** Peers inspect each other's permitted Git branches, PR diffs and shared filesystem worktrees, exchange verified APIs through `[REQUEST]` / `[ANSWER]`, and settle routine contract questions directly. Do not require Orchestrator ACK for normal DTO adjustments or source comparison.
- **Exchange real paths.** Where a common workspace exists, each lane posts a `[WORKSPACE]` containing its *verified* absolute path, branch, HEAD, dirty state, and local build tools. Prefer nearby separate worktrees rather than a shared mutable checkout. Never delete, reset or modify someone else's dirty files, index or branch. Use agreed local commits, patches or cherry-picks into one's **own** worktree for integration.
- **Resolve shared ownership once.** Only one editor writes to an overlapping shared subtree; agents can claim/acknowledge the edit ownership in the issue and read or review each other's work. Escalate only an actual overlap, security-contract conflict or destructive decision. Peers can continue independently safe work while one dependency is unavailable.
- **Autonomy covers the whole outcome.** After assignment, each agent decomposes and implements the substantial slice, compiles/builds/tests locally as real Project tools allow, fixes errors and continues. Reports focus on changed shared contracts, integration milestones and real blockers; no one-comment-per-command or one-approval-per-fix rituals.
- **Local-first / large-PR when selected.** Keep intermediate development and locally integrated commits in owned worktrees. Perform available local run, build and focused validation first, inspect the accumulated integration diff, and publish a substantial PR/release only when its coherent functional block is ready under the Project's actual Git rules. Do not create routine PR/CI/deploy/Issue churn for every small change. Lack of a local tool limits the claimed validation level; it does not justify inventing results.
- **Review meaningful boundaries.** Orchestrator resolves material contradictions, unsafe data or secret changes, new privileged infrastructure scope and integrated acceptance, rather than preapproving each PR or patch. A partial handoff documents a subset, not completion of the entire work ID. Keep SOURCE/STATIC, BUILD, LOCAL_RUNTIME, DEV_RUNTIME, authenticated authorization and production readiness distinct.

## Blocked-agent fallback: useful refactoring

A real dependency block need not make a specialist idle. **First** check whether some other safe, independently executable part of the current release/MVP objective remains, and ask the owning peer directly for the exact missing contract. Only when meaningful critical-path progress is genuinely unavailable may an agent use that otherwise idle time for lower-priority engineering improvements.

- Prefer **small, behavior-preserving refactoring** inside the lane's own code: remove duplicated paths, simplify unnecessary abstractions, correct misleading boundaries and names, reduce maintenance costs, or improve diagnosed error handling. Inspect existing peer code read-only to avoid incompatible changes. Do not turn a temporary wait into speculative architecture or optimization work.
- Inspect tests only with a concrete purpose: retire provably obsolete/redundant checks without removing required CI or safety coverage; add targeted checks for a demonstrated risky method when beneficial. Do not create an expansive new test program merely to fill idle time. Follow the active Project's actual testing policy.
- Keep the work in the existing owned local branch and work ID, preserve known-good behavior, avoid destructive/deployment/credential changes and unnecessary PR/Issue churn. One concise status may identify the genuine blocker, refactoring slice, and evidence; reusable lessons can flow into the existing workspace learning register rather than a new tracker.
- **Resume the primary release path immediately** once unblocked. Unfinished optional refactoring is deferred; it must not delay a functional milestone or be reported as product acceptance. Distinguish local source/build evidence from deployed and authenticated runtime proof.

## Workspace issue lifecycle and learning capture

When a Project uses one long-running issue as the temporary shared workspace, distinguish its **type** from ordinary defects. A simple optional title prefix such as `[Workspace]` identifies a coordination + context-collection hub; `[Task]`, `[Bug]`, `[Audit]`, `[Cleanup]` can distinguish other issue intents without imposing a new label taxonomy or creating tickets for minor changes. The Project selects actual names; this role only defines their meanings.

- **A workspace is disposable task state, not disposable knowledge.** Its issue body is the editable index of active work, decisions, role owners and links. Per-agent comments and related Git refs are source evidence. A workspace can outlive an MVP release while unresolved tasks and reusable lessons are being reconciled. Closing is allowed only after evidence-based acceptance and knowledge migration; deletion is not a prerequisite.
- **Collect lessons during ordinary work, not as another blocker.** Give each lane one discoverable, bounded learning section/comment. Agents note a real mistake, wrong approach, effective tool/worktree/coordination pattern, or material correction when already reporting a milestone: *symptom or technique → cause → change → observed result and validation level → immutable comment/commit link*. Distinguish verified behavior from a hypothesis and avoid routine command logs, credentials or redundant cross-lane copies. No extra ACK, new issue, PR or pause of implementation for collecting a lesson.
- **Editable index, append-only evidence.** Where a provider supports editing, agents may revise their own collection comments. If the connected interface cannot edit issue comments, add concise linked lesson deltas; Orchestrator periodically consolidates them into the editable workspace body. Never claim that an immutable issue comment was edited or erase provenance. Keep the index concise and use stable lane-specific learning IDs.
- **Promote once, at the right owner.** At stabilization or completion, deduplicate per-lane findings and classify each as **reusable rule**, **project-only contract**, **duplicate**, **unverified**, or **rejected**. Generalize only supported multi-project lessons to the existing role/skill/audit owner under `../audit/CONTEXT_MAINTENANCE.md`; leave product-specific facts in their Project authority. Compress wording, preserve one canonical meaning and links to evidence, and avoid automatically promoting every local incident into a universal rule.
- **Closure gate.** Before marking a workspace archived/closed, reconcile all lanes' meaningful findings and remaining work IDs, record target rule paths/commit IDs and accepted scope, perform required independent review, and verify that no unique supported lesson was lost. Leave it open when promotion, validation or handoff remains unresolved. Only the workspace index changes during this reconciliation, not a duplicated repository task database.

## Stabilization and fan-in

After functional slices converge, run an explicit stabilization/fan-in pass when the change is large enough to justify it:

- inspect the complete accumulated diff;
- resolve duplicate implementations and ownership drift;
- run the applicable non-destructive validation required by project policy;
- synchronize state/docs/contracts;
- record remaining blockers and validation level;
- hand the exact reviewed head/diff to the independent Reviewer when required.

Do not blindly repeat every check each executor already ran; validate the integrated risk surface.

## Publication

Publication cadence follows the Project's release policy; in a local-first Project, publish once a substantial integrated feature has been checked as far as local tools allow, not after every correction. Publication authority still follows the repository/tool contract. In the standard GitHub split, the Implementer/writer owns branches, commits and PR revisions; the independent Reviewer reviews and merges. Orchestrator does not bypass protected branches, required checks, access scope or that identity separation. A development deployment is not authorization to deploy to production.

## Completion

Do not claim the coordinated task complete until every required slice is `done` or explicitly `blocked`, fan-in is stable, shared authorities are synchronized and required review/acceptance gates are evidenced. For an issue-backed task, update the issue's current-state index and record a final acceptance or reasoned changes request with revision, scope and evidence; close only the accepted work item.
