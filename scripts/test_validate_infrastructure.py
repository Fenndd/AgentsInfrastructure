"""Regression tests for the optional source checker; no product test suite."""
from pathlib import Path
import tempfile
import unittest

import validate_infrastructure as checker


POLICY = """# Synthetic routing fixture
| Tier | Model | Effort |
| --- | --- | --- |
| 1 | GPT-6 Luna (`gpt-6-luna`) | max (always) |
| 2 | GPT-6.1 Sol (`gpt-6.1-sol`) | medium |
| 3 | GPT-6.1 Sol (`gpt-6.1-sol`) | high |
| 4 | GPT-6 Astra (`gpt-6-astra`) | high |

| Tier | Preset | Model | Effort | Selection within tier |
| --- | --- | --- | --- | --- |
| 1 | `sonnet-high` | Sonnet 5.5 | high | Determined. |
| 2 | `sonnet-high` | Sonnet 5.5 | high | Default. |
| 3 | `opus-medium` | Opus 5.5 | medium | Focused. |
| 3 | `opus-high` | Opus 5.5 | high | Focused with limited checks. |
| 4 | `opus-max` | Opus 5.5 | max | Exceptional. |
"""

CODEX_FRAGMENT = '''[agents]
default_subagent_model = "gpt-6.1-sol"
default_subagent_reasoning_effort = "medium"
'''


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, text=""):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def routing_fixture(self):
        self.write("docs/engineering/AI_ORCHESTRATION.md", POLICY)
        for name, model, effort in (
            ("sonnet-high", "claude-sonnet-5-5", "high"),
            ("opus-medium", "claude-opus-5-5", "medium"),
            ("opus-high", "claude-opus-5-5", "high"),
            ("opus-max", "claude-opus-5-5", "max"),
        ):
            self.write(f".claude/agents/{name}.md", f"---\nname: {name}\nmodel: {model}\neffort: {effort}\n---\n")

    def skills_fixture(self):
        self.write(".agents/skills/example/SKILL.md", '---\nname: "example"\ndescription: "Synthetic skill."\n---\n')
        self.write(".claude/skills/example/SKILL.md", "---\nname: example\ndescription: Synthetic skill.\n---\nRead [canonical](../../../.agents/skills/example/SKILL.md).\n")

    def test_broken_real_link_detected_with_line_number(self):
        self.write("README.md", "# Fixture\n[broken](missing.md#fragment)\n")
        self.assertEqual(checker.check_links(self.root), ["README.md:2: broken local link: missing.md#fragment"])

    def test_fenced_code_external_fragments_and_illustrations_ignored(self):
        self.write("README.md", """```markdown
[example](missing.md)
```
~~~
[another](also-missing.md)
~~~
[external](https://example.test/missing.md)
[fragment](#future)
`docs/future.md` and `[illustrative](not-real.md)`
""")
        self.assertEqual(checker.check_links(self.root), [])

    def test_real_relative_encoded_link_checked(self):
        self.write("docs/a file.md")
        self.write("README.md", "[valid](docs/a%20file.md#section)\n[bad](docs/no%20file.md)\n")
        errors = checker.check_links(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("docs/no%20file.md", errors[0])

    def test_adapter_metadata_and_canonical_target(self):
        self.skills_fixture()
        self.assertEqual(checker.check_skills(self.root), [])
        self.write(".claude/skills/example/SKILL.md", "---\nname: example\ndescription: Drift.\n---\n[wrong](../../../.agents/skills/other/SKILL.md)\n")
        errors = checker.check_skills(self.root)
        self.assertTrue(any("adapter description" in error for error in errors))
        self.assertTrue(any("canonical SKILL.md" in error for error in errors))

    def test_preset_and_fixed_inventory_drift(self):
        self.routing_fixture()
        self.assertEqual(checker.check_routing(self.root), [])
        path = self.root / ".claude/agents/opus-high.md"
        path.write_text(path.read_text().replace("effort: high", "effort: medium"))
        self.write(".claude/agents/extra.md", "---\nname: extra\n---\n")
        errors = checker.check_routing(self.root)
        self.assertTrue(any("opus-high" in error for error in errors))
        self.assertTrue(any("inventory" in error for error in errors))

    def test_optional_config_fixed_defaults_and_invalid_toml(self):
        self.routing_fixture()
        self.write("presets/codex-config.toml", CODEX_FRAGMENT)
        self.assertEqual(checker.check_routing(self.root), [])
        self.write("presets/codex-config.toml", CODEX_FRAGMENT.replace('"medium"', '"high"'))
        self.assertTrue(any("fixed gpt-6.1-sol" in error for error in checker.check_routing(self.root)))
        self.write("presets/codex-config.toml", 'model = "unterminated')
        self.assertTrue(any("invalid TOML" in error for error in checker.check_routing(self.root)))

    def test_source_fragment_rejects_main_session_count_and_permission_settings(self):
        self.routing_fixture()
        for fragment in (
            'model = "gpt-6.1-sol"\nmodel_reasoning_effort = "medium"\n',
            'model = "gpt-6.1-terra"\n' + CODEX_FRAGMENT,
            CODEX_FRAGMENT + 'max_threads = 4\n',
            'approval_policy = "never"\n' + CODEX_FRAGMENT,
            'sandbox_mode = "workspace-write"\n' + CODEX_FRAGMENT,
            CODEX_FRAGMENT + '[permissions]\nnetwork = true\n',
        ):
            with self.subTest(fragment=fragment):
                self.write("presets/codex-config.toml", fragment)
                self.assertTrue(any("expected only [agents]" in error for error in checker.check_routing(self.root)))

    def test_policy_drift_detected_even_when_preset_is_also_changed(self):
        self.routing_fixture()
        self.write("docs/engineering/AI_ORCHESTRATION.md", POLICY.replace("gpt-6-luna", "gpt-6-other").replace("Sonnet 5.5", "Sonnet 6.0"))
        errors = checker.check_routing(self.root)
        self.assertTrue(any("Codex policy" in error for error in errors))
        self.assertTrue(any("Claude policy" in error for error in errors))

    def test_payload_sources_and_validation_do_not_mutate_tree(self):
        self.routing_fixture()
        self.skills_fixture()
        self.write("presets/codex-config.toml", CODEX_FRAGMENT)
        for source in checker.REQUIRED_SOURCES:
            path = self.root / source
            if source.endswith("/"):
                path.mkdir(parents=True, exist_ok=True)
            elif not path.exists():
                self.write(source)
        inventory = "| Source | Destination | Purpose |\n| --- | --- | --- |\n"
        inventory += "".join(f"| `{source}` | Same path | Fixture |\n" for source in sorted(checker.REQUIRED_SOURCES))
        self.write("README.md", inventory)
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(checker.validate(self.root), [])
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        (self.root / "GEMINI.md").unlink()
        self.assertTrue(any("does not exist: GEMINI.md" in error for error in checker.check_payload(self.root)))


if __name__ == "__main__":
    unittest.main()
