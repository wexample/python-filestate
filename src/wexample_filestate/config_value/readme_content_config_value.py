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

    Sections are discovered automatically from template files across all search
    paths. Order is controlled via `readme.sections` in the suite config.yml.
    Each section is rendered independently and joined — no blank line pollution.
    """

    @staticmethod
    def _format_dependencies_list(dependencies: list[str]) -> str:
        return "\n".join([f"- {dep}" for dep in dependencies])

    def get_templates(self) -> list[str] | None:
        """Render each section independently and join with double newlines."""
        from wexample_helpers.helpers.string import string_ensure_end_with_new_line

        context = self._get_template_context()
        section_names = self._get_section_names()

        exclude_from_toc = {"title", "table-of-contents"}
        available_sections = []
        for name in section_names:
            if name not in exclude_from_toc and self._section_exists(name):
                available_sections.append(
                    {
                        "name": name,
                        "title": self._section_name_to_title(name),
                        "anchor": name.replace("_", "-"),
                    }
                )
        context["available_sections"] = available_sections

        parts = []
        for name in section_names:
            rendered = self._render_section(name, context)
            if rendered and rendered.strip():
                parts.append(rendered.strip())

        content = "\n\n".join(parts)
        if content:
            content = string_ensure_end_with_new_line(content)

        return [content]

    def _get_readme_search_paths(self) -> list[Path]:
        return []

    def _get_section_names(self) -> list[str]:
        return []

    def _get_template_context(self) -> dict:
        return {}

    def _register_jinja_filters(self, env: Environment) -> None:
        from wexample_helpers.helpers.string import string_convert_case_map

        for key, func in string_convert_case_map().items():
            env.filters[f"to_{key}"] = func

    def _render_section(self, section_name: str, context: dict) -> str | None:
        """Render a single section. Tries .md.j2 then .md across all search paths."""
        from jinja2 import Environment, FileSystemLoader, TemplateNotFound

        for search_path in self._get_readme_search_paths():
            if not search_path.exists():
                continue
            env = Environment(loader=FileSystemLoader(str(search_path)))
            self._register_jinja_filters(env)
            try:
                return env.get_template(f"{section_name}.md.j2").render(context)
            except TemplateNotFound:
                pass

        for search_path in self._get_readme_search_paths():
            md_path = search_path / f"{section_name}.md"
            if md_path.exists():
                env = Environment(loader=FileSystemLoader(str(search_path)))
                self._register_jinja_filters(env)
                return env.from_string(md_path.read_text(encoding="utf-8")).render(context)

        return None

    def _section_exists(self, section_name: str) -> bool:
        for search_path in self._get_readme_search_paths():
            if (search_path / f"{section_name}.md.j2").exists():
                return True
            if (search_path / f"{section_name}.md").exists():
                return True
        return False

    def _section_name_to_title(self, section_name: str) -> str:
        return section_name.replace("-", " ").replace("_", " ").title()
