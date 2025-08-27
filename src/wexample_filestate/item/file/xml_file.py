from __future__ import annotations

from typing import ClassVar

from wexample_filestate.item.file.structured_content_file import StructuredContentFile
from wexample_helpers.const.types import StructuredData


class XmlFile(StructuredContentFile):
    EXTENSION_XML: ClassVar[str] = "xml"

    def _expected_file_name_extension(self) -> str:
        return self.EXTENSION_XML

    # ---------- Parsing / Serialization ----------
    def loads(self, text: str, strict: bool = False) -> StructuredData:
        import xmltodict
        try:
            parsed = xmltodict.parse(text)
            return parsed or {}
        except Exception as e:
            if strict:
                raise e
            return {}

    def dumps(self, value: StructuredData | None) -> str:
        import xmltodict
        if isinstance(value, str):
            # Already XML string
            return value
        try:
            return xmltodict.unparse(value or {}, pretty=True)
        except Exception:
            return str(value)
