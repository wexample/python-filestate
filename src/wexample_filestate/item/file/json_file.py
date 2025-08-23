from __future__ import annotations

from typing import ClassVar

from wexample_filestate.item.file.structured_content_file import StructuredContentFile
from wexample_helpers.const.types import JsonContent, StructuredData


class JsonFile(StructuredContentFile):
    EXTENSION_JSON: ClassVar[str] = "json"

    def _expected_file_name_extension(self) -> str:
        return self.EXTENSION_JSON

    def _parse_file_content(self, content: str) -> JsonContent:  # type: ignore[name-defined]
        import json

        try:
            return json.loads(content)
        except Exception:
            return {}

    def _prepare_content_to_write(self, content: StructuredData) -> str:
        import json

        # Pretty print while keeping unicode characters intact
        return json.dumps(content, ensure_ascii=False, indent=2)
