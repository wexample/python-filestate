from __future__ import annotations

from typing import ClassVar

from wexample_filestate.item.file.structured_content_file import StructuredContentFile
from wexample_helpers.const.types import StructuredData


class HtmlFile(StructuredContentFile):
    EXTENSION_HTML: ClassVar[str] = "html"
    EXTENSION_HTM: ClassVar[str] = "htm"

    def _expected_file_name_extension(self) -> str:
        return self.EXTENSION_HTML

    def _parse_file_content(self, content: str) -> str:
        # We keep HTML as raw string by default. If callers need a parsed tree,
        # they can pass a BeautifulSoup object to write(), which will be cast to str.
        return content

    def writable(self, content: StructuredData | None = None) -> str:
        content = content or self.read()

        # Accept string content or any object convertible to string (e.g., BeautifulSoup)
        return content if isinstance(content, str) else str(content)
