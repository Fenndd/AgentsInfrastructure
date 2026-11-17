# AI Development Infrastructure

This folder is the source template for the user's AI-assisted development infrastructure. Maintain reusable instructions and processes here, then transfer them to an existing or new project when the user requests it. No concrete product is developed here.

The infrastructure contains shared repository rules, task and verification workflows, task-based model routing, Claude Code model/effort presets, and reusable skills. It does not install clients, configure accounts, or enable tools and permissions. Active user and session instructions take precedence.

## Transfer Payload

Paths in the destination are relative to its project root.

| Source | Destination | Purpose |
| --- | --- | --- |
| `templates/AGENTS.md` | `AGENTS.md` | Shared rules; merge with an existing project's rules |
| `CLAUDE.md` | `CLAUDE.md` | Claude entrypoint to `AGENTS.md` |
| `GEMINI.md` | `GEMINI.md` | Gemini entrypoint to `AGENTS.md` |
| `.agents/skills/` | `.agents/skills/` | Canonical skills, references, metadata, and included licenses |
| `.claude/skills/` | `.claude/skills/` | Thin adapters to the canonical skills |
| `.claude/agents/` | `.claude/agents/` | Four roleless model/effort presets |
| `docs/engineering/AI_ORCHESTRATION.md` | Same path | Delegation tiers, model preferences, context handoff, verification |
| `docs/engineering/DEVELOPMENT_WORKFLOW.md` | Same path | From request to result, checks, decisions, handoff |
| `docs/engineering/TASK_FORMAT.md` | Same path | Milestones, task files, dependencies, acceptance and status format |
| `.editorconfig` | `.editorconfig` | Shared text-formatting defaults; merge with existing settings |
| `.gitattributes` | `.gitattributes` | Text and line-ending defaults; merge with existing settings |
| `.gitignore` | Merge relevant rules into `.gitignore` | Local secrets, client overrides, worktrees, personal editor state |

Do not copy this folder's root `AGENTS.md`, `README.md`, `templates/` directory, or [transfer procedure](docs/engineering/INFRASTRUCTURE_TRANSFER.md) into a product as product files. They govern and explain the infrastructure source. The contents of `templates/AGENTS.md` become the destination's root rules.

## Included Skills

| Skill | Purpose |
| --- | --- |
| `model-routing` | Choose a delegation tier, model/effort, and bounded handoff when delegation is useful |
| `session-teacher` | Guided understanding of a development session when requested |
| `security-best-practices` | Explicitly requested security guidance or reviews for supported languages/frameworks |
| `security-threat-model` | Explicitly requested, repository-grounded threat modeling |

Each skill's `SKILL.md` defines its trigger and workflow. Installation alone does not start a review, a teaching session, or a subagent. Framework-specific security references are reusable guidance, not a required product stack.

The working defaults are GPT-6.1 Sol at medium effort in Codex and Sonnet 5.5 at high effort in Claude Code. The Claude presets are `sonnet-high`, `opus-medium`, `opus-high`, and `opus-max`. They request fixed Sonnet 5.5 or Opus 5.5 versions and explicit effort values. Routing preferences and client-specific behavior are owned by [AI_ORCHESTRATION.md](docs/engineering/AI_ORCHESTRATION.md). Check the actual session's capabilities before launching agents; the stored preferences do not guarantee model availability or override client-level restrictions.

## Usage

Ask the agent to transfer or update this infrastructure in a named destination project. Follow [INFRASTRUCTURE_TRANSFER.md](docs/engineering/INFRASTRUCTURE_TRANSFER.md) for both new and existing projects.

Inspect and merge existing instructions and settings. Preserve project-specific facts, work in progress, unrelated skills, and existing permissions. Add only confirmed destination-specific context pointers to `AGENTS.md`. Requirements, decisions, status, roadmap, and tasks are created or adapted for the destination's actual work; no product backlog is bundled here.

Updates to this source do not automatically update other projects. Changes made for one destination do not become shared policy unless the user requests that change to the source.

## Maintenance and Verification

Edit the canonical skill or shared process and retain thin client adapters. Keep third-party references, attribution, and included licenses with their skills. Do not import personal/global configuration as mandatory project policy.

For documentation and infrastructure changes, inspect the changed content, resolve relative local links, compare adapter skill names and descriptions with their canonical files, and check preset/routing consistency. For a transfer, also inspect the destination diff and run its existing relevant checks when the changes affect them. Report checks performed and limitations; do not invent a runtime test suite for this template.
