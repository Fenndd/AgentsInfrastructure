# Transferring the AI Infrastructure

This procedure belongs to the infrastructure source. Use it when the user requests installation or an update in a particular destination. The source [README](../../README.md) owns the payload inventory.

## Inspect the Destination

1. Confirm the requested destination and inspect its current files, applicable instructions, and Git state if it is a repository. For a new folder, verify that it is the intended location before creating files.
2. Read existing `AGENTS.md`, client entrypoints, relevant skills/presets, process documents, and text/Git configuration that the payload would affect. Check nested instructions for affected paths.
3. Identify the actual project's requirements, architecture records, setup/check commands, and workflow if they exist. Do not use facts from another project or invent missing facts.
4. Separate reusable infrastructure from destination-specific decisions. Resolve material contradictions with the user's current request; do not silently discard existing rules or unfinished work.

The transfer request authorizes the necessary local infrastructure edits. It does not by itself authorize committing, pushing, publishing, deleting existing work, changing permissions, or installing external tools.

## Apply the Payload

1. Use `templates/AGENTS.md` as the shared baseline for the destination's root `AGENTS.md`. Merge existing project rules and add relevant, verified context pointers. Do not copy the infrastructure source's root `AGENTS.md`.
2. Copy or merge only the payload paths listed in the source README. Preserve unrelated destination files. When an infrastructure file already differs, compare its behavior and rationale before editing; do not replace directories wholesale.
3. Keep `.agents/skills/` canonical. Retain each skill's supporting references, metadata, and licenses. Keep `.claude/skills/` as thin entrypoints with matching names and descriptions and working relative paths.
4. Retain the four roleless Claude presets and keep their tier, fixed model version, and effort values consistent with the orchestration policy. Preserve unrelated presets. If destination constraints require different routing, record the deliberate adaptation without changing the source implicitly.
5. Merge `CLAUDE.md` and `GEMINI.md` so they include the shared rules once and retain any valid destination-specific instructions.
6. Merge `.editorconfig`, `.gitattributes`, and `.gitignore` without losing existing rules, exceptions, or binary-file handling. Do not add stack-specific ignores without evidence from the destination.
7. Adapt process-document references only as needed for the destination's confirmed conventions. Preserve existing requirements, ADRs, tasks, roadmap, and current status. Do not create fictitious tasks or completion records just to match a template.

Do not transfer product source, dependencies, runtime configuration, `.env` values, credentials, datasets, models, caches, session records, Git history, or personal client settings as part of this infrastructure. Do not change the source project during a transfer unless the user also requests that change.

## Verify and Report

- Review the final destination diff, or compare affected files if Git is unavailable. Confirm that unrelated work and project-specific rules are preserved.
- Verify local links and client includes from their destination locations. Separate literal example paths and optional future documents from required files.
- Compare each Claude skill adapter's `name` and `description` with its canonical skill, and check that the canonical target and referenced resources exist.
- Check tier/model/effort consistency across the orchestration tables, model-routing entrypoints, and Claude presets. Check current tool capabilities if actual execution is requested; copied preferences alone are not execution evidence.
- Search changed infrastructure for stale source-project names, absolute local paths, product-specific requirements, and task/status history.
- Run existing relevant destination checks if affected. For an instructions-only transfer, content, link, consistency, and diff checks are normally sufficient.
- Report what was installed or merged, deliberate adaptations, actual checks and results, and anything not verified. Do not claim that an AI client loaded the files or that a preset executed unless that was observed.

Future synchronization is another explicit transfer/update request. Compare the latest source with the destination again; do not assume that the destination has stayed unchanged.
