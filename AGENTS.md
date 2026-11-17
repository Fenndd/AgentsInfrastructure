# AI Infrastructure Source Rules

This folder is the canonical source template for AI-assisted development infrastructure. It is maintained here and transferred to existing or new projects only when the user requests it. No concrete product is developed in this folder.

Read [templates/AGENTS.md](templates/AGENTS.md) for the shared working rules. Paths in that template describe the root of a destination project; while maintaining this source, resolve those paths from this folder's root.

## Maintaining This Source

- Keep shared agent instructions, skills, client adapters, model/effort presets, and development-process documentation here.
- Do not introduce a product's source code, dependencies, requirements, architecture decisions, tasks, roadmap, current status, data, credentials, generated outputs, or session history.
- Keep reusable rules independent of a product name, technology stack, machine path, or particular development task. Generic examples and framework-specific skill references are allowed; they do not select a destination project's stack.
- Preserve a single canonical copy of each shared process. Claude Code skill entrypoints refer to `.agents/skills/`; they do not duplicate the canonical skills.
- Make general working-rule changes in `templates/AGENTS.md`. This root file adds only the rules for maintaining the infrastructure source and must not replace a destination project's `AGENTS.md`.
- Keep the payload inventory and transfer procedure in [README.md](README.md) and [INFRASTRUCTURE_TRANSFER.md](docs/engineering/INFRASTRUCTURE_TRANSFER.md) consistent with the files.
- Do not automatically modify projects that have received this infrastructure. A transfer or update requires the user's request for the destination.
- For a requested transfer, follow the transfer procedure, inspect the destination, preserve its existing work and project-specific rules, and verify the result.

No product `STATUS.md`, `ROADMAP.md`, or task backlog is needed here. The workflow and task-format documents describe how destination projects may organize development.
