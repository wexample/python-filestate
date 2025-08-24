from __future__ import annotations

from typing import ClassVar

from wexample_filestate.item.file.structured_content_file import StructuredContentFile
from wexample_helpers.const.types import StructuredData


class EnvFile(StructuredContentFile):
    """
    Simple .env reader/writer using python-dotenv.
    """

    EXTENSION_ENV: ClassVar[str] = "env"

    def _expected_file_name_extension(self) -> str:
        return self.EXTENSION_ENV

    def read(self) -> StructuredData:
        # Delegate parsing to python-dotenv without touching os.environ
        from dotenv import dotenv_values

        return dict(dotenv_values(self.get_path()))
