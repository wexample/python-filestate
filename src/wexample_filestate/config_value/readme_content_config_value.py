from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.config_value.aggregated_templates_config_value import (
    AggregatedTemplatesConfigValue,
)

if TYPE_CHECKING:
    from pathlib import Path


@base_class
class ReadmeContentConfigValue(AggregatedTemplatesConfigValue):
    def get_templates(self) -> list[str] | None:
        """Generate README content from templates.

        This method orchestrates the entire README generation process.
        """
        context = self._get_template_context()
        section_names = self._get_section_names()

        # Collect available sections
        available_sections = []
        for section_name in section_names:
            if section_name not in ["title", "table-of-contents"]:
                if self._section_exists(section_name):
                    available_sections.append(
                        {
                            "name": section_name,
                            "title": self._section_name_to_title(section_name),
                            "anchor": section_name.replace("_", "-"),
                        }
                    )

        context["available_sections"] = available_sections

        # Render in order
        rendered_content = ""
        for section_name in section_names:
            section_content = self._render_readme_section(section_name, context)
            if section_content:
                rendered_content += f"{section_content}\n\n"

        return [rendered_content]

    def _format_dependencies_list(self, dependencies: list[str]) -> str:
        """Format dependencies as a Markdown list.

        Args:
            dependencies: List of dependency strings

        Returns:
            Formatted Markdown list
        """
        return "\n".join([f"- {dep}" for dep in dependencies])

    def _get_bundled_templates_path(self) -> Path:
        """Return the path to bundled default templates.

        Must be implemented by subclasses.
        """
        raise NotImplementedError(
            "Subclasses must implement _get_bundled_templates_path()"
        )

    def _get_project_dependencies(self) -> list[str]:
        doc = self.workdir.get_project_config()
        project = doc.get("project", {}) if isinstance(doc, dict) else {}
        return project.get("dependencies", [])

    def _get_project_description(self) -> str:
        """Return the project description.

        Must be implemented by subclasses.
        """
        raise NotImplementedError(
            "Subclasses must implement _get_project_description()"
        )

    def _get_project_homepage(self) -> str:
        """Return the project homepage URL.

        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement _get_project_homepage()")

    def _get_project_license(self) -> str:
        """Return the project license information.

        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement _get_project_license()")

    def _get_readme_search_paths(self) -> list[Path]:
        """Return list of paths to search for README templates.

        Generic implementation that searches in:
        1. Workdir-specific templates
        2. Suite-level templates (if available)
        3. Bundled default templates

        Returns:
            List of paths to search for templates
        """
        from wexample_app.const.globals import WORKDIR_SETUP_DIR

        workdir_path = self.workdir.get_path()
        search_paths = [
            workdir_path / WORKDIR_SETUP_DIR / "knowledge" / "readme",
        ]

        # Suite-level templates
        suite_path = self.workdir.find_suite_workdir_path()
        if suite_path is not None:
            search_paths.append(
                suite_path / WORKDIR_SETUP_DIR / "knowledge" / "package-readme"
            )

        # Default templates (bundled)
        bundled_path = self._get_bundled_templates_path()
        if bundled_path is not None:
            search_paths.append(bundled_path)

        return search_paths

    def _get_section_names(self) -> list[str]:
        """Return the list of section names to include in the README.

        Default sections common to all packages. Subclasses can override
        to add language-specific sections.

        Returns:
            List of section names in order
        """
        return [
            "title",
            "table-of-contents",
            "status-compatibility",
            "prerequisites",
            "installation",
            "quickstart",
            "basic-usage",
            "configuration",
            "logging",
            "api-reference",
            "examples",
            "tests",
            "code-quality",
            "versioning",
            "changelog",
            "migration-notes",
            "roadmap",
            "troubleshooting",
            "security",
            "privacy",
            "support",
            "contribution-guidelines",
            "maintainers",
            "license",
            "useful-links",
            "suite-integration",
            "compatibility-matrix",
            "requirements",
            "dependencies",
            "links",
            "suite-signature",
        ]

    def _get_suite_workdir_path(self) -> Path | None:
        """Return the suite workdir path if available.

        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement _get_suite_workdir_path()")

    def _get_template_context(self) -> dict:
        """Build the template context with all variables.

        Generic implementation with common variables. Subclasses should
        override and call super() to add language-specific variables.

        Returns:
            Dictionary of template variables
        """
        return {
            # filestate: python-iterable-sort
            "dependencies": self._get_project_dependencies(),
            "description": self._get_project_description(),
            "deps_list": self._format_dependencies_list(
                self._get_project_dependencies()
            ),
            "license_info": self._get_project_license(),
            "homepage": self._get_project_homepage(),
            "package_name": self.workdir.get_package_name(),
            "project_name": self.workdir.get_project_name(),
            "version": self.workdir.get_project_version(),
            "workdir": self.workdir,
        }

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
