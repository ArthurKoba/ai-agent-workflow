# New Project Playbook

A concise decision and acceptance checklist for starting a service intended for AI-agent-driven development. This is a **playbook**, not an additional runtime instruction layer or a replacement for task skills. Follow the authoritative source linked at each step; read only the relevant modules when a task requires them.

## 1. Define the service before generating code

- [ ] Specify the service's purpose, boundaries, interfaces, expected workload, deployment target and measurable acceptance criteria. Prefer one specialized AI Project per independently developed service; define shared cross-service contracts in one neutral authority instead of copying them into each repository.
- [ ] Research mature, well-documented open-source implementations and libraries before inventing an architecture. Reuse compatible, license-appropriate designs rather than starting from imagination.
- [ ] Choose language by workload and demonstrated constraints: default to **Python** for rapid prototyping and general services; consider **Go** when concurrency or operational efficiency justifies it; reserve **Rust** for resource-critical components with measured benefits that offset its higher agent-development cost.
- [ ] Make dependencies and external services explicit. Prefer maintained, documented open-source components; validate fit before adopting them.

See [software engineering](../skills/software-engineering/README.md), [context engineering](../skills/context-engineering.md), and [system architecture](../docs/SYSTEM_ARCHITECTURE.md).

## 2. Bootstrap a strict, reproducible repository

- [ ] Set up the language-appropriate toolchain, pinned versions, lockfile, environments, formatting, typing, linting, tests, build and CI **before** substantial feature development. For new Python use **uv**; for new TypeScript use **Bun**, subject to existing-project migration rules.
- [ ] Enable the strictest *applicable* quality gates, including limits that prevent oversized functions and excessive complexity, to push agents toward decomposition. Use justified, targeted exceptions rather than disabling checks globally.
- [ ] Install and **verify active** tracked Git hooks: mandatory full relevant quality gate on `pre-push`, independent CI checks, and fail-closed behavior. Keep fast development checks distinct from release/merge acceptance; do not run the full suite after every trivial edit.
- [ ] Make local setup, checks and execution reproducible for a fresh checkout.

**Authority:** [project bootstrap](../skills/project-bootstrap.md). For implementation-specific standards use the relevant [software](../skills/software-engineering/README.md) or [frontend](../skills/frontend-engineering/README.md) module, not another copy here.

## 3. Establish agent context without duplicating state

- [ ] Configure universal **Account** instructions for cross-project decision behavior only; **Project** instructions for sources of authority, tool/MCP routing, permissions, local-context policy and validation ownership. Neither should contain a static stack inventory, architecture dump or facts easily recovered from the repository.
- [ ] Add a short repository `AGENTS.md` as an entry map: where to find the canonical project map, contracts, task state and applicable skills. Do not repeat injected prompts or copy entire skills into it.
- [ ] Let source own implementation details, documentation own durable contracts and navigation, infrastructure own operational state, and Issues/Work Items own tasks, decisions, blockers and handoffs. Do not build a parallel Markdown backlog or transient state log.
- [ ] Integrate this workflow library by **linking** to relevant skills; load complete selected mandatory sources just in time, not the whole library at every startup.

**Authorities:** [runtime hierarchy](../README.md), [prompt sources](../prompts/README.md), [context engineering](../skills/context-engineering.md), [Git and Issues](../skills/git-workflow.md).

## 4. Design and implement in bounded passes

- [ ] Analyze substantial changes at least twice: first goals, existing implementation, constraints and candidate solutions; second assumptions, alternatives and failure modes. Add a third pass for high-risk work.
- [ ] Design responsibilities, boundaries, typed contracts, data models and integration points before broad implementation. Apply extra design/review passes when complexity demands them.
- [ ] Implement in coherent batches, followed by scoped checks, grouped defect correction and recheck. Avoid full lint/test cycles for each micro-edit; perform early targeted checks when correctness or irreversible risk demands them.
- [ ] For Python API-oriented services, prefer async **FastAPI**, **SQLAlchemy** and **Pydantic** typed validation at boundaries where appropriate; consider lighter internal `dataclass`/`NamedTuple` representations only when evidence justifies it. For frontend, prefer **Vue** and maintained UI component/design-system libraries over unnecessary custom HTML/UI components. Preserve existing project conventions unless migration is explicitly in scope.
- [ ] Separate implementation, architectural, contract, performance and style review passes when they need different context. Use independent Implementer/Reviewer roles where required.

**Authorities:** [account behavior source](../prompts/accounts/universal.md) (reference for prompt design, **not** mandatory rereading at runtime), [software engineering](../skills/software-engineering/README.md), [frontend engineering](../skills/frontend-engineering/README.md), [context engineering](../skills/context-engineering.md), [roles](../roles/README.md).

## 5. Integrate and deploy

- [ ] Use the Git workflow permitted by actual repository protections and tool permissions: direct push only when allowed; otherwise working branch → PR/MR → independent review → merge. A prototype may use a simplified workflow, never bypass required gates.
- [ ] Prefer reproducible Compose for straightforward service packaging where it fits; CI can run quality gates while Coolify builds, or deployment can use a prebuilt immutable image when provenance/rollback requirements justify it; use the existing service manager/orchestrator for deployed infrastructure, rather than imposing a second control plane. Check deployment, readiness, persistence, rollback and runtime acceptance at the relevant boundary.
- [ ] Keep current task state in Issues, durable changes in code/contracts, and deployment details in their owning infrastructure source.

**Authorities:** [Git workflow](../skills/git-workflow.md), [service deployment](../skills/services-deployment/README.md), [MCP strategy](../docs/MCP_STRATEGY.md).

## 6. Improve the agent system from evidence

- [ ] Examine recurring agent errors, costly context reloads, redundant tool calls and effective solutions after meaningful phases.
- [ ] Classify the underlying cause and assign the correction to the **smallest correct owner**: project configuration, skill, role, quality gate or specialized MCP. Promote to universal Account rules only if genuinely cross-project.
- [ ] Prefer structured, validated MCP tools for repetitive, error-prone or privilege-sensitive operations. Do not add new prompt rules or skills when an existing owner already covers the decision.
- [ ] Preserve reusable findings through the audit process, without copying execution logs or transient project state into this library.

**Authorities:** [workflow audit](../audit/README.md), [context maintenance](../audit/CONTEXT_MAINTENANCE.md), [MCP strategy](../docs/MCP_STRATEGY.md).

## Ready-to-start gate

A new service is ready for agent-led implementation when its boundaries and acceptance criteria are defined; the repository is reproducible with enforced quality gates; authoritative code, contract, infrastructure and Issue owners are clear; and Account → Project → on-demand skill routing works without duplicating state. Confirm actual checks rather than treating the presence of configuration files as proof.
