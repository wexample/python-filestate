from __future__ import annotations

from typing import ClassVar

from wexample_filestate.item.file.structured_content_file import StructuredContentFile
from wexample_helpers.const.types import StructuredData
from wexample_helpers_toml.const.types import TomlContent  # type: ignore


class TomlFile(StructuredContentFile):
    EXTENSION_TOML: ClassVar[str] = "toml"

    def _expected_file_name_extension(self) -> str:
        return self.EXTENSION_TOML

    def _parse_file_content(self, content: str) -> StructuredData:  # type: ignore[name-defined]
        # Prefer the widely used 'toml' package for both load and dump symmetry.
        # If you prefer stdlib reading, replace with 'tomllib' and pair with 'tomli_w' for writing.
        import toml

        try:
            return toml.loads(content)
        except Exception:
            return {}

    def _prepare_content_to_write(self, content: StructuredData) -> str:
        import toml

        return toml.dumps(content)
