# Transferring the AI Infrastructure

This procedure belongs to the infrastructure source. Use it when the user requests installation or an update in a particular destination. The source [README](../../README.md) owns the payload inventory.

## Inspect the Destination

1. Confirm the requested destination and inspect its current files, applicable instructions, and Git state if it is a repository. For a new folder, verify that it is the intended location before creating files.
2. Read existing `AGENTS.md`, client entrypoints, relevant skills/presets, process documents, and text/Git configuration that the payload would affect. Check nested instructions for affected paths.
3. Identify the actual project's requirements, architecture records, setup/check commands, and workflow if they exist. Do not use facts from another project or invent missing facts.
4. Separate reusable infrastructure from destination-specific decisions. Resolve material contradictions with the user's current request; do not silently discard existing rules or unfinished work.
5. Look for a prior transfer receipt at the destination's `docs/engineering/INFRASTRUCTURE_PROVENANCE.md`. When its baseline is available, compare three versions for affected paths: that prior source baseline, the latest requested source, and the current destination. Distinguish upstream changes from destination adaptations before merging. If the baseline or receipt is missing, say so and compare the available source and destination directly; do not reconstruct an unverified baseline.

The transfer request authorizes the necessary local infrastructure edits. It does not by itself authorize committing, pushing, publishing, deleting existing work, changing permissions, or installing external tools.

## Apply the Payload

1. Use `templates/AGENTS.md` as the shared baseline for the destination's root `AGENTS.md`. Merge existing project rules and add relevant, verified context pointers. Do not copy the infrastructure source's root `AGENTS.md`.
2. Copy or merge only the payload paths listed in the source README. Preserve unrelated destination files. When an infrastructure file already differs, compare its behavior and rationale before editing; do not replace directories wholesale.
3. Keep `.agents/skills/` canonical. Retain each skill's supporting references, metadata, and licenses. Keep `.claude/skills/` as thin entrypoints with matching names and descriptions and working relative paths.
4. Retain the four roleless Claude presets and keep their tier, fixed model version, and effort values consistent with the orchestration policy. Preserve unrelated presets. If destination constraints require different routing, record the deliberate adaptation without changing the source implicitly.
5. Merge `CLAUDE.md` and `GEMINI.md` so they include the shared rules once and retain any valid destination-specific instructions.
6. Merge `.editorconfig`, `.gitattributes`, and `.gitignore` without losing existing rules, exceptions, or binary-file handling. Do not add stack-specific ignores without evidence from the destination.
7. Adapt process-document references only as needed for the destination's confirmed conventions. Preserve existing requirements, ADRs, tasks, roadmap, and current status. Do not create fictitious tasks or completion records just to match a template.
8. Include the generic [evaluation procedure](AI_INFRASTRUCTURE_EVALUATION.md) from the README payload inventory. Its checks are optional aids; they do not establish product requirements or require product tooling. The optional `scripts/validate_infrastructure.py` and `scripts/test_validate_infrastructure.py` remain source-only maintenance helpers, use the Python standard library, and are not required transfer payload. Do not copy them into a product merely to make its infrastructure complete.
9. Install `presets/codex-config.toml` as the destination's `.codex/config.toml` only when the destination uses a supporting Codex client and a compatibility and merge check succeeds. Inspect existing project configuration first; preserve unrelated settings. Retain the fixed GPT-6.1 Sol / medium default when installing the template. Do not change global configuration, permissions, sandbox or approval settings, or agent-count limits as part of this optional config. If unsupported or conflicting, leave the optional template uninstalled and record why.
10. Review files retired from the latest source against the prior receipt and current destination. They may contain destination work or still serve a purpose. Report retirement candidates and the chosen disposition; do not automatically delete them or unrelated files.
11. Create or update the destination's `docs/engineering/INFRASTRUCTURE_PROVENANCE.md` with the source baseline, the paths actually installed or merged, deliberate adaptations, omitted optional paths, and verification results. Use the example below as a format, not as a receipt to create in this source folder.

Do not transfer product source, dependencies, runtime configuration, `.env` values, credentials, datasets, models, caches, session records, Git history, or personal client settings as part of this infrastructure. Do not change the source project during a transfer unless the user also requests that change.

## Destination Transfer Receipt

The receipt records what was transferred and supports later comparisons. A source revision identifies a baseline; it does not prove that an AI client loaded instructions, honored configuration, or executed the requested model. Record observed client behavior separately when it was actually checked. If the source has uncommitted changes, record the base revision and that fact with a description of the transferred differences; do not describe a revision alone as the exact installed source.

Example to adapt in the destination, using actual values and installed paths:

```markdown
# Infrastructure Provenance

- Transfer date: <actual date>
- Source: <canonical source identity>
- Source baseline: <revision or version; note uncommitted differences if any>
- Prior installed baseline: <revision/version, or unavailable>

## Installed or Merged Paths

| Source path | Destination path | Outcome |
| --- | --- | --- |
| templates/AGENTS.md | AGENTS.md | Merged shared rules with existing project rules |
| <actual source path> | <actual destination path> | <installed, merged, or updated> |

List the complete installed payload, including actual skill and adapter paths.

## Deliberate Adaptations and Omissions

- <destination-specific adaptation and reason>
- <optional path omitted and reason, or none>
- <retired path reviewed and disposition, or none>

## Verification

- <actual content, link, consistency, and diff checks and results>
- Client loading/configuration execution: <observed evidence, or not verified>
```

## Verify and Report

- Review the final destination diff, or compare affected files if Git is unavailable. Confirm that unrelated work and project-specific rules are preserved.
- Verify local links and client includes from their destination locations. Separate literal example paths and optional future documents from required files.
- Compare each Claude skill adapter's `name` and `description` with its canonical skill, and check that the canonical target and referenced resources exist.
- Check tier/model/effort consistency across the orchestration tables, model-routing entrypoints, and Claude presets. Check current tool capabilities if actual execution is requested; copied preferences alone are not execution evidence.
- If the optional Codex configuration was installed, verify the supported project configuration location and syntax, the merged diff, and its fixed Sol / medium default. Distinguish configuration presence from observed client loading and effective execution settings.
- Search changed infrastructure for stale source-project names, absolute local paths, product-specific requirements, and task/status history.
- Run existing relevant destination checks if affected. For an instructions-only transfer, content, link, consistency, and diff checks are normally sufficient.
- Verify that the provenance receipt matches the actual installed paths and adaptations, identifies the source accurately, and records any missing prior baseline. Review retirement candidates explicitly; do not treat absence from the newest payload as deletion authority.
- Report what was installed or merged, deliberate adaptations, actual checks and results, and anything not verified. Do not claim that an AI client loaded the files or that a preset executed unless that was observed.

Future synchronization is another explicit transfer/update request. Use the prior receipt's source baseline when available to compare baseline, latest source, and current destination again; do not assume that the destination has stayed unchanged. Preserve prior transfer evidence when updating the receipt rather than silently replacing the identity of the installed baseline.
