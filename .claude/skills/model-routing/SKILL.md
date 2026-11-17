---
name: model-routing
description: Identify useful independent subagent tasks, then choose the working-default model or a justified exception with bounded context handoffs. Keep small sequential tasks in the main session.
---

# Project Model Routing (Claude Code entrypoint)

The canonical skill is shared with Codex. Read [.agents/skills/model-routing/SKILL.md](../../../.agents/skills/model-routing/SKILL.md) and the shared [orchestration policy](../../../docs/engineering/AI_ORCHESTRATION.md), then follow them.

Claude Code adaptation: determine the tier with the policy's "Choosing a Tier" rule, then use the "Choosing a Model in Claude Code" table. The `sonnet-high` preset serves both tiers 1 and 2; choose `opus-medium` or `opus-high` within tier 3 by the table's explicit condition, and `opus-max` only after the tier-4 gate. Launch the matching roleless preset from `.claude/agents/` as the agent type, without passing `model` or `effort`: per-call values would replace the preset's. State the tier and the instruction to read the policy in every brief. Session tool rules take precedence.
