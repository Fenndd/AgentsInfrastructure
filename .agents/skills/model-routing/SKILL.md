---
name: model-routing
description: Identify useful independent subagent tasks, then choose the working-default model or a justified exception with bounded context handoffs. Keep small sequential tasks in the main session.
---

# Project Model Routing

Read the shared [orchestration policy](../../../docs/engineering/AI_ORCHESTRATION.md) before selecting a subagent. That document owns the model preferences, project constraints, handoff modes, and reporting requirements; do not copy them into client-specific profiles.

For substantial work, identify independent bounded parts before choosing models. Delegate the useful parts, in parallel where allowed, without a target agent count. Tier 2 is the working default; use tier 1 for fully determined work, tier 3 for a specific reasoning gap, and tier 4 only after documenting every condition of its gate. Take the model and effort from your client's table. In Codex, pass both `model` and `reasoning_effort` in the spawn call with `fork_turns: "none"`; in Claude Code, launch the selected preset. Apply the current tool's supported parameters and context-fork rules. This skill provides instructions, not an automatic model switch or enforced router.

Give the worker its tier, the instruction to read the policy before starting, a concrete question or result, minimal source pointers, read-only or exact editing boundaries, and observable completion criteria. Prefer compact evidence for reading tasks and direct changes to assigned files for writing tasks. Verify the relevant original sources, resulting diff, and actual checks before integration. Keep the main agent responsible for product decisions and the final result.
