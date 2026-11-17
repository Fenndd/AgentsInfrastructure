# Working with Subagents

## When to Delegate

For a substantial task, identify bounded parts that can proceed independently before choosing models: targeted source reading, implementation in separate areas, checking another hypothesis, or independent review. Delegate each useful independent part when its expected benefit justifies startup and coordination. Launch independent parts in parallel when the tools allow it; do not bundle them into one broad assignment merely to reduce the number of agents. Simple edits and tightly dependent sequential steps usually stay in the main session. There is no target agent count.

Choose the model for each delegated part, not for the whole project or the parent task. Most delegated work should use the working default in [Choosing a Tier](#choosing-a-tier). If one narrow question needs stronger reasoning, isolate that question and keep the other parts on the default. The main agent owns product decisions and integration.

Define roles and tasks for the current task. Do not create fixed profiles such as `explorer`, `worker`, `reviewer`, or similar in advance. Choose the number of agents based on useful independent tasks and environment constraints, rather than trying to use every available slot.

## Choosing a Tier

Every delegated task gets exactly one tier, 1–4. Start at tier 2, the working default. Move to tier 1 only when the answer or change is fully determined by a source or existing pattern. Move to tier 3 only for a specific reasoning difficulty. Tier 4 is an exceptional, separately justified choice. The client tables map tiers to model and effort; they do not set the main session's model.

| Tier | Use for the delegated task |
| --- | --- |
| 1 — determined | Locate facts in named sources or apply an existing pattern with no meaningful choice between approaches. A direct comparison, search, or existing check can verify the result. |
| 2 — working default | Implement, diagnose, review, test, or document a bounded result when the expected behavior and a meaningful way to check it are known or can be established through a bounded investigation. This can involve multiple files or components and normal implementation judgment. |
| 3 — targeted difficulty | Resolve a specific uncertain contract or interaction, compare competing causes or designs, or reconcile conflicting evidence that tier 2 cannot settle through its ordinary bounded investigation. State the exact reasoning question in the brief. |
| 4 — exceptional | Use only when **all** conditions in [The tier-4 gate](#the-tier-4-gate) hold. Assign a focused question, not an entire feature or broad review. |

Apply the same rule to implementation, diagnosis, and review. A topic's label — security, concurrency, persistence, migration, or architecture — does not set the tier by itself. High consequences call for stronger checks and independent verification; they do not automatically call for a stronger model. File count, context size, output volume, the parent model, and the project's overall importance do not set the tier either.

If the brief lacks the expected behavior, a reference, or a check, first determine whether the main agent can supply it or delegate a bounded investigation. Missing requirements, data, or access are not model-escalation reasons. When the tier is uncertain, identify the actual reasoning gap; use tier 2 if a bounded investigation can resolve it, and tier 3 only if the gap meets its condition. A failed attempt warrants escalation only when its evidence shows reasoning difficulty, not merely an incomplete or incorrect first result.

### The tier-4 gate

Before selecting tier 4, record all of the following in the task brief:

1. The narrow question or artifact that needs the exceptional model, with its boundaries.
2. The specific reasoning difficulty, such as interacting constraints or unresolved contradictory evidence, that makes tier 3 inadequate. A failed tier-3 attempt is useful evidence but is not required when the difficulty is clear in advance.
3. Why an incorrect answer would be costly or hard to detect **and** why the available checks or independent review at tier 3 cannot adequately resolve that difficulty.
4. How the main agent will inspect or test the answer before integrating it.

If any condition is absent, use tier 3 or below and strengthen verification as needed. Do not escalate the entire task because one part passes this gate. If a tier-4 attempt fails, return the unresolved issue to the main agent instead of repeating the same broad request.

## Choosing a Model in Codex

The preferred working model for the main Codex session is GPT-6.1 Sol at medium effort when the client allows that choice. For subagents, assess reasoning difficulty, context volume, risk, and expected output volume separately. A large input or output does not by itself require a stronger reasoning model.

Determine the tier with [Choosing a Tier](#choosing-a-tier), then use this table. The combinations below are project routing preferences, not launch settings, quality guarantees, or verified pricing rankings. Check the available models and effort values in the current session. They concern development assistants, not any model the product itself may use.

| Tier | Model | Effort |
| --- | --- | --- |
| 1 | GPT-6 Luna (`gpt-6-luna`) | max (always) |
| 2 | GPT-6.1 Sol (`gpt-6.1-sol`) | medium |
| 3 | GPT-6.1 Sol (`gpt-6.1-sol`) | high |
| 4 | GPT-6 Astra (`gpt-6-astra`) | high |

In Codex (desktop app or CLI), the spawn call is the single mechanism: pass both `model` and `reasoning_effort` from the tier's row, with `fork_turns: "none"`, and never leave either to be inherited. A full-history fork (`"all"`) inherits the parent's settings and ignores overrides. Codex has no preset files, so the brief must carry the tier and the duties in [Subagent Duties](#subagent-duties); the task brief defines the role. The table guides subagents and does not change the main session's model or effort.

Tier 2 is the default for substantive delegated work. Select Sol `high` only for the particular tier-3 reasoning question, and Astra only when the tier-4 gate is satisfied. For Luna, always use `max`; do not lower it to `high`, `medium`, or `low`. Do not change tier to economize or to match the parent session's model. Use actual pricing and usage evidence when comparing monetary costs; the table alone does not rank prices.

The table guides subagent requests; it does not switch the main session's model. Keep product decisions, ownership of tightly coupled concurrency and security changes, and final integration with the main agent. A bounded independent review or a specific reasoning question from such work can still be delegated.

If the result is uncertain or a check fails, determine the cause before retrying. Improve the brief or verification when either is inadequate; escalate only when the remaining obstacle is reasoning difficulty. Do not repeat ineffective attempts indefinitely.

## Choosing a Model in Claude Code

The preferred working model for the main Claude Code session is Sonnet 5.5 at high effort when the client provides that version. Determine the tier with [Choosing a Tier](#choosing-a-tier), then use the table. Tier 1 and the tier-2 working default both use Sonnet 5.5 `high`. Use Opus only for a specific tier-3 or tier-4 question. Do not recommend Haiku or Fable. Delegate only as the session's tool rules allow.

| Tier | Preset | Model | Effort | Selection within tier |
| --- | --- | --- | --- | --- |
| 1 | `sonnet-high` | Sonnet 5.5 | high | Determined work. |
| 2 | `sonnet-high` | Sonnet 5.5 | high | Working default. |
| 3 | `opus-medium` | Opus 5.5 | medium | Targeted reasoning difficulty with meaningful checks. |
| 3 | `opus-high` | Opus 5.5 | high | The same focused difficulty when an error has serious consequences or checks cover only part of the answer. State why `medium` is inadequate. |
| 4 | `opus-max` | Opus 5.5 | max | Only after the tier-4 gate. |

The four roleless presets in [.claude/agents/](../../.claude/agents/) request fixed model versions and effort values; the brief defines the task. Launch the selected preset by its agent type and pass neither `model` nor `effort`, because per-call overrides would replace its values. Check that the fixed version is supported by the active Claude Code client before launching and verify the actual model and effort when the client reports them. The table guides subagent requests; it does not switch the main session's model.

## Environment Capabilities

Before launching, check which models, effort values, and context handoff methods are actually available. Set the selected parameters explicitly when the interface supports it. Do not promise that an override will be applied if the tool only inherits the parent session's settings.

If a combination is unavailable, do not silently substitute a model alias, version, or effort. Keep useful work in the main session or choose another available combination only when the user's instructions permit that substitution, and report the difference. For Gemini, use the same task-based selection principle without inventing model equivalencies with Codex or carrying over unsupported parameters.

This document does not enable or configure the subagent mechanism. It does not expand tool permissions, authorize external data sharing, or override active session limitations.

## Task Definition and Coordination

Give the subagent the goal, required sources, editing boundaries or read-only mode, result criteria, expected checks, its tier, and the instruction to read this policy before starting. Add the last two in every client, even when a preset already states them. For tier 3, name the specific reasoning question; for tier 4, include the gate's four reasons and verification plan. Provide enough context while avoiding unnecessary copying of the entire history.

Use a short task-specific brief instead of a full-history fork when history is not necessary. Check the interface before selecting a model: in the current collaboration interface a full-history fork inherits the parent's settings and does not accept overrides. This interface-specific limitation must be rechecked when the tools change.

For parallel edits, assign different file areas. Perform dependent changes sequentially; the main agent integrates shared files. Use a separate checkout only when isolation is genuinely needed. Do not create multiple workers for the same implementation without a reason.

The main agent checks findings, integrates the result, and is responsible for the overall verification. A subagent's “done” message alone does not confirm that the task is complete.

## Subagent Duties

These apply to every subagent in every client (Claude Code, Codex, or another), whatever the model or preset.

1. Before any other action, read this policy in full.
2. Check the task against [Choosing a Tier](#choosing-a-tier). If tier 1 lacks a determining source or pattern, or tier 2 lacks an expected result or a meaningful check that can be established through bounded investigation, report the gap before making changes. If a specific question truly needs tier 3, or the full tier-4 gate holds, stop and report the evidence to the main agent; do not silently upgrade yourself. A task that turns out to be simpler than its assigned tier is completed as assigned.
3. Do only the task in the brief, within its read-only mode or editing boundaries. Do not make product decisions.
4. Follow [Data Handling](#data-handling) and the reading or writing mode below, and report in the form the brief and this policy require.

## Reading and Writing with Bounded Context

For context gathering, assign a concrete question and relevant paths in read-only mode. Ask for findings with file/symbol references, verified line locations where useful, contradictions, and remaining uncertainty. Do not return entire files or a generic repository summary. The main agent reads the necessary original sections before editing or accepting a significant conclusion; a summary may omit important conditions and line numbers must be checked.

For repetitive generation, provide an existing reference, the target paths, behavior criteria, and meaningful checks. Have the subagent write directly to the assigned files and return the changed paths, a short explanation, actual check results, and unresolved issues. The main agent inspects the diff and relevant implementation without requiring the full generated text in the chat. If a pattern does not exist, define it first rather than asking a worker to invent architecture. Do not create boilerplate or tests merely to exercise delegation.

These modes describe task shapes, not permanent agent roles or separate required skills. No file-size threshold forces delegation or blocks a necessary targeted read.

## Data Handling

Do not send secrets, credentials, personal data, or other confidential content to development assistants or external services. Use permitted synthetic fixtures, source code without secrets, and content-free measurements. Development routing does not change the product's own data-processing requirements.

## Scope and Evidence

The project-local [model-routing skill](../../.agents/skills/model-routing/SKILL.md) is a Codex entrypoint to this shared policy; [.claude/skills/model-routing](../../.claude/skills/model-routing/SKILL.md) is the Claude Code entrypoint to the same skill. Claude Code uses its own model table and the subagent presets in `.claude/agents/`; there is no one-to-one mapping between the Codex and Claude tables. Other clients use this document through the existing repository instructions; no global configuration is changed.

This is advisory routing through existing subagent tools. Apart from the Claude Code model/effort presets, no Portal service, custom router plugin, hook, MCP server, API dependency, or telemetry system is configured. Reconsider enforced routing only after actual repeated inefficient operations and a tested integration justify it. Codex supports [plugin hooks](https://developers.openai.com/plugins/build/plugins), but that does not establish an installed or trusted hook in this checkout.

The source idea is discussed in [Spotify's Shunt article](https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90): bounded reading and direct file generation reduce the primary agent's context. Its reported savings are specific to its benchmark, not a measured reduction in this project's total tokens, latency, or cost. A single shared policy and a small entrypoint follow [OpenAI's guidance on focused skills](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).

## Transparency

In the final report on substantial delegation, state the task, selected model and effort, a brief reason for the choice, the result, and how it was checked. If the tool does not expose the actual execution parameters, say so; do not present requested parameters as confirmed.

Include elapsed time and token usage only when the tool actually reports them. Mark unavailable metrics as unavailable; do not estimate savings from model names or present worker-only token counts as total workflow usage. Use the existing task report and `STATUS.md` for significant results rather than creating a parallel activity log.
