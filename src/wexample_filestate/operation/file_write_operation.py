from __future__ import annotations

from wexample_filestate.operation.abstract_existing_file_operation import (
    AbstractExistingFileOperation,
)
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class FileWriteOperation(AbstractExistingFileOperation):
    content: str = public_field(
        description="The content to write",
    )

    def apply(self) -> None:
        self._target_file_write(content=self.content)

    def describe_after(self) -> str:
        return "The file content has been updated according to configuration."

    def describe_before(self) -> str:
        return "The file content needs to be updated."

    def description(self) -> str:
        return "Write or update file content with specified content."
