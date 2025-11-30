from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.config_value.aggregated_templates_config_value import (
    AggregatedTemplatesConfigValue,
)


@base_class
class ReadmeContentConfigValue(AggregatedTemplatesConfigValue):
    def get_templates(self) -> list[str] | None:
        return []

    def _get_readme_search_paths(self) -> list:
        """Return list of paths to search for README templates.
        
        Must be implemented by subclasses.
        """
        raise NotImplementedError(
            "Subclasses must implement _get_readme_search_paths()"
        )

    def _render_readme_section(self, section_name: str, context: dict) -> str | None:
        """Render a README section from template files.
        
        Searches for section_name.md.j2 (Jinja2 template) first,
        then falls back to section_name.md (plain Markdown with Jinja2 variables).
        
        Args:
            section_name: Name of the section to render
            context: Template context variables
            
        Returns:
            Rendered section content or None if not found
        """
        from jinja2 import Environment, FileSystemLoader, TemplateNotFound

        search_paths = self._get_readme_search_paths()

        # Try .md.j2 first
        for search_path in search_paths:
            if not search_path.exists():
                continue

            env = Environment(loader=FileSystemLoader(str(search_path)))
            try:
                template = env.get_template(f"{section_name}.md.j2")
                return template.render(context)
            except TemplateNotFound:
                pass

        # Then try .md
        for search_path in search_paths:
            md_path = search_path / f"{section_name}.md"
            if md_path.exists():
                content = md_path.read_text(encoding="utf-8")
                env = Environment(loader=FileSystemLoader(str(search_path)))
                template = env.from_string(content)
                return template.render(context)

        return None

    def _section_exists(self, section_name: str) -> bool:
        """Check if a README section template exists.
        
        Args:
            section_name: Name of the section to check
            
        Returns:
            True if section template exists, False otherwise
        """
        for search_path in self._get_readme_search_paths():
            if (search_path / f"{section_name}.md.j2").exists():
                return True
            if (search_path / f"{section_name}.md").exists():
                return True
        return False

    def _section_name_to_title(self, section_name: str) -> str:
        """Convert a section name to a human-readable title.
        
        Args:
            section_name: Section name with dashes or underscores
            
        Returns:
            Title-cased string with spaces
        """
        return section_name.replace("-", " ").replace("_", " ").title()
