from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.config_value.aggregated_templates_config_value import (
    AggregatedTemplatesConfigValue,
)

if TYPE_CHECKING:
    from pathlib import Path

    from jinja2 import Environment


@base_class
class ReadmeContentConfigValue(AggregatedTemplatesConfigValue):
    """Base class for README content generation.

    Renders _README.tpl.j2 found in the search paths. That template controls
    section order via {% include %} directives with bare section names
    (e.g. {% include "installation" ignore missing %}).

    The custom loader resolves bare names to .md.j2 then .md across all
    search paths in priority order.
    """

    @staticmethod
    def _format_dependencies_list(dependencies: list[str]) -> str:
        return "\n".join([f"- {dep}" for dep in dependencies])

    def get_templates(self) -> list[str] | None:
        """Render _README.tpl.j2, building available_sections from its includes."""
        from jinja2 import Environment, TemplateNotFound

        search_paths = self._get_readme_search_paths()
        existing_paths = [p for p in search_paths if p.exists()]

        if not existing_paths:
            return None

        env = Environment(loader=self._make_section_loader(existing_paths))
        self._register_jinja_filters(env)

        try:
            tpl = env.get_template("_README.tpl.j2")
        except TemplateNotFound:
            return None

        context = self._get_template_context()
        context["available_sections"] = self._build_available_sections(env)

        return [tpl.render(context)]

    def _make_section_loader(self, search_paths: list):
        """Jinja2 loader that resolves bare section names to .md.j2 or .md.

        For a name with no extension (e.g. "installation"), tries:
          installation.md.j2 then installation.md across all search paths.
        Explicit filenames (_README.tpl.j2, title.md.j2) resolve normally.
        First match across paths wins.
        """
        from pathlib import Path

        from jinja2 import BaseLoader, TemplateNotFound

        paths = [Path(p) for p in search_paths]

        class SectionLoader(BaseLoader):
            def get_source(self, environment, template):
                has_ext = "." in template
                candidates = (
                    [template]
                    if has_ext
                    else [f"{template}.md.j2", f"{template}.md"]
                )
                for path in paths:
                    for candidate in candidates:
                        full = path / candidate
                        if full.exists():
                            source = full.read_text(encoding="utf-8")
                            mtime = full.stat().st_mtime
                            return (
                                source,
                                str(full),
                                lambda: full.stat().st_mtime == mtime,
                            )
                raise TemplateNotFound(template)

        return SectionLoader()

    def _build_available_sections(self, env) -> list[dict]:
        """Return TOC metadata for sections declared in _README.tpl.j2.

        Reads include directives from the tpl source to preserve order.
        Excludes structural sections (title, table-of-contents).
        Only includes sections whose template actually resolves.
        """
        import re

        from jinja2 import TemplateNotFound

        exclude = {"title", "table-of-contents"}
        available = []
        seen: set[str] = set()

        try:
            source, _, _ = env.loader.get_source(env, "_README.tpl.j2")
        except TemplateNotFound:
            return available

        for match in re.finditer(
            r"""{%-?\s*include\s+['"]([^'"]+)['"]\s*""", source
        ):
            name = match.group(1)
            if name.endswith(".md.j2"):
                section = name[: -len(".md.j2")]
            elif name.endswith(".md"):
                section = name[: -len(".md")]
            else:
                section = name

            if section in exclude or section in seen:
                continue

            try:
                env.get_template(section)
                seen.add(section)
                available.append(
                    {
                        "name": section,
                        "title": self._section_name_to_title(section),
                        "anchor": section.replace("_", "-"),
                    }
                )
            except TemplateNotFound:
                pass

        return available

    def _get_readme_search_paths(self) -> list[Path]:
        return []

    def _get_template_context(self) -> dict:
        return {}

    def _register_jinja_filters(self, env: Environment) -> None:
        from wexample_helpers.helpers.string import string_convert_case_map

        for key, func in string_convert_case_map().items():
            env.filters[f"to_{key}"] = func

    def _section_name_to_title(self, section_name: str) -> str:
        return section_name.replace("-", " ").replace("_", " ").title()
