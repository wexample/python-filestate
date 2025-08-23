from __future__ import annotations

from typing import ClassVar

from wexample_filestate.item.file.structured_content_file import StructuredContentFile
from wexample_helpers.const.types import StructuredData


class XmlFile(StructuredContentFile):
    EXTENSION_XML: ClassVar[str] = "xml"

    def _expected_file_name_extension(self) -> str:
        return self.EXTENSION_XML

    def _parse_file_content(self, content: str) -> StructuredData:
        import xmltodict

        try:
            parsed = xmltodict.parse(content)
            return parsed or {}
        except Exception:
            return {}

    def _prepare_content_to_write(self, content: StructuredData) -> str:
        import xmltodict

        if isinstance(content, str):
            # Already XML string
            return content

        try:
            # xmltodict expects a mapping-like object
            return xmltodict.unparse(content, pretty=True)
        except Exception:
            # Fallback to string representation if content is not mappable
            return str(content)
