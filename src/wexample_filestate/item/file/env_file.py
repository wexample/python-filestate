from __future__ import annotations

from typing import ClassVar

from wexample_filestate.item.file.structured_content_file import StructuredContentFile
from wexample_helpers.const.types import StructuredData


class EnvFile(StructuredContentFile):
    """
    Simple .env reader/writer using python-dotenv.
    """

    EXTENSION_ENV: ClassVar[str] = "env"
    EXTENSION_DOT_ENV: ClassVar[str] = f".{EXTENSION_ENV}"

    def _expected_file_name_extension(self) -> str:
        return self.EXTENSION_ENV

    def read(self, reload: bool = True) -> StructuredData:
        # Delegate parsing to python-dotenv without touching os.environ
        from dotenv import dotenv_values

        return dict(dotenv_values(self.get_path()))

    def _prepare_content_to_write(self, content: StructuredData) -> str:
        # Unused now that write() is overridden. Keep a no-op textual fallback.
        if not isinstance(content, dict):
            return ""
        return (
            "\n".join(f"{k}={v if v is not None else ''}" for k, v in content.items())
            + "\n"
        )
