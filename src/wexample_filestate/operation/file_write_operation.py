from __future__ import annotations

from wexample_filestate.operation.abstract_existing_file_operation import (
    AbstractExistingFileOperation,
)


class FileWriteOperation(AbstractExistingFileOperation):
    @staticmethod
    def _join_with_original_newline(lines: list[str], original: str) -> str:
        """Join lines using \n and preserve a trailing newline if present in original."""
        trailing_newline = original.endswith("\n")
        updated = "\n".join(lines)
        if trailing_newline and (updated or original.splitlines()):
            updated += "\n"
        return updated

    def describe_after(self) -> str:
        return "The file content has been updated according to configuration."

    def describe_before(self) -> str:
        return "The file content needs to be updated."

    def description(self) -> str:
        return "Write or update file content with specified content."
