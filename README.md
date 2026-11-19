# AI Development Infrastructure

A reusable process template for AI-assisted software development with Claude Code, Codex and Gemini CLI.

- **Problem:** AI coding agents work well only with clear rules, task boundaries and verification. Writing these rules again for every repository leads to drift between projects.
- **What it provides:** one canonical set of repository rules, a task format with acceptance criteria, a development and review workflow, model and effort routing for subagents, four portable skills, and a behavioral evaluation procedure.
- **How it is used:** the agent transfers the payload into a product repository on request and records a provenance receipt there. A standard-library Python checker verifies links, adapter drift and preset consistency (see [Maintenance and Verification](#maintenance-and-verification)).

Own content is MIT-licensed ([LICENSE](LICENSE)); bundled third-party skills keep their licenses ([NOTICE.md](NOTICE.md)).

This folder is the source template for the user's AI-assisted development infrastructure. Maintain reusable instructions and processes here, then transfer them to an existing or new project when the user requests it. No concrete product is developed here.

The infrastructure contains shared repository rules, task and verification workflows, task-based model routing, Claude Code model/effort presets, reusable skills, and a behavioral evaluation procedure. An optional Codex configuration fragment supplies executor defaults in compatible clients. It does not install clients, configure accounts, or enable tools and permissions. Active user and session instructions take precedence.

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
| `presets/codex-config.toml` | Merge into `.codex/config.toml` only when compatible | Optional working-default executor settings; preserve unrelated settings |
| `docs/engineering/AI_ORCHESTRATION.md` | Same path | Delegation tiers, model preferences, context handoff, verification |
| `docs/engineering/DEVELOPMENT_WORKFLOW.md` | Same path | From request to result, checks, decisions, handoff |
| `docs/engineering/TASK_FORMAT.md` | Same path | Milestones, task files, dependencies, acceptance and status format |
| `docs/engineering/AI_INFRASTRUCTURE_EVALUATION.md` | Same path | Repeatable routing scenarios, evidence levels, and comparison method |
| `.editorconfig` | `.editorconfig` | Shared text-formatting defaults; merge with existing settings |
| `.gitattributes` | `.gitattributes` | Text and line-ending defaults; merge with existing settings |
| `.gitignore` | Merge relevant rules into `.gitignore` | Local secrets, client overrides, worktrees, personal editor state |

Do not copy this folder's root `AGENTS.md`, `README.md`, `templates/` or `presets/` directories, `scripts/`, or [transfer procedure](docs/engineering/INFRASTRUCTURE_TRANSFER.md) into a product as product files. They govern and verify the infrastructure source. The contents of `templates/AGENTS.md` become the destination's root rules; the optional preset is merged into its listed destination rather than copied as a directory. Create a destination provenance receipt as described in the transfer procedure; no destination history belongs here.

## Included Skills

| Skill | Purpose |
| --- | --- |
| `model-routing` | Delegate coherent results, schedule parallel or sequential stages, and choose a justified tier with bounded handoffs |
| `session-teacher` | Guided understanding of a development session when requested |
| `security-best-practices` | Explicitly requested security guidance or reviews for supported languages/frameworks |
| `security-threat-model` | Explicitly requested, repository-grounded threat modeling |

Each skill's `SKILL.md` defines its trigger and workflow. Installation alone does not start a review, a teaching session, or a subagent. Framework-specific security references are reusable guidance, not a required product stack.

Only the four listed skills are bundled. User-global skills or plugins available in the maintainer's session are not transferred or guaranteed in a destination. Discover the actual skill catalog there; add another portable skill only for a demonstrated reusable need, with its canonical resources and adapters.

The orchestrator and working executor have distinct responsibilities. The fixed working defaults remain GPT-6.1 Sol medium and Sonnet 5.5 high; [AI_ORCHESTRATION.md](docs/engineering/AI_ORCHESTRATION.md) owns orchestrator settings, model tables, tier gates, and launch details. The Claude presets remain `sonnet-high`, `opus-medium`, `opus-high`, and `opus-max`. Select coherent assignments before scheduling them; dependent stages may be delegated sequentially. Stronger models resolve justified narrow questions, then ordinary follow-up returns to the working default. There is no prescribed agent count or artificial limit.

Check actual session capabilities and relevant overrides before launching. Stored preferences and optional defaults do not prove which settings executed or override client restrictions. The Codex fragment is kept outside `.codex/` so maintaining this source does not silently activate project settings.

## Usage

Ask the agent to transfer or update this infrastructure in a named destination project. Follow [INFRASTRUCTURE_TRANSFER.md](docs/engineering/INFRASTRUCTURE_TRANSFER.md) for both new and existing projects.

Inspect and merge existing instructions and settings. Preserve project-specific facts, work in progress, unrelated skills, and existing permissions. Add only confirmed destination-specific context pointers to `AGENTS.md`. Requirements, decisions, status, roadmap, and tasks are created or adapted for the destination's actual work; no product backlog is bundled here.

Updates to this source do not automatically update other projects. Changes made for one destination do not become shared policy unless the user requests that change to the source.

## Maintenance and Verification

Edit the canonical skill or shared process and retain thin client adapters. Keep third-party references, attribution, and included licenses with their skills. Do not import personal/global configuration as mandatory project policy.

For documentation and infrastructure changes, inspect the changed content, resolve relative local links, compare adapter skill names and descriptions with their canonical files, and check preset/routing consistency. For a transfer, also inspect the destination diff and run its existing relevant checks when affected.

The optional source-only [static checker](scripts/validate_infrastructure.py) uses Python 3.11+ and its standard library. Python is not required to use or transfer the instructions. From this source root:

```powershell
python -B scripts/validate_infrastructure.py
python -B -m unittest discover -s scripts -p 'test_validate_infrastructure.py' -v
```

The [checker tests](scripts/test_validate_infrastructure.py) use disposable synthetic fixtures to verify detection of broken links, metadata/configuration drift, and accidental mutation. These are infrastructure checks, not a product runtime test suite. The checker does not establish client loading, model execution, or effective usage savings. Use [the behavioral evaluation procedure](docs/engineering/AI_INFRASTRUCTURE_EVALUATION.md) for those questions and keep experiment records in the test destination. Report actual checks and limitations.
