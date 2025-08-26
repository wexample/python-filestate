from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_filestate.item.file.structured_content_file import StructuredContentFile

if TYPE_CHECKING:
    from tomlkit import TOMLDocument


class TomlFile(StructuredContentFile):
    EXTENSION_TOML: ClassVar[str] = "toml"

    def _expected_file_name_extension(self) -> str:
        return self.EXTENSION_TOML

    def _parse_file_content(self, content: str) -> TOMLDocument:
        # Use tomlkit to preserve comments and formatting during round-trip
        from tomlkit import document, parse

        try:
            if content is None or content == "":
                # Return an empty TOMLDocument to keep types consistent
                return document()
            return parse(content)
        except Exception:
            # On parse error, return an empty TOMLDocument instead of a dict
            return document()

    def make_writable_content(self, content: TOMLDocument | dict | None) -> str:
        """Serialize a TOMLDocument (preferred) or a plain dict to TOML.
        Using tomlkit.dumps preserves comments/formatting when content is a TOMLDocument.
        """
        from tomlkit import document, dumps

        try:
            if content is None:
                return dumps(document())
            return dumps(content)
        except Exception:
            # As a safe fallback, write an empty TOML document
            return dumps(document())
