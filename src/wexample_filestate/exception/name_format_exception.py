from __future__ import annotations

from typing import ClassVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.exception.abstract_file_state_exception import (
    AbstractFileStateException,
)


@base_class
class NameFormatException(AbstractFileStateException):
    """Exception raised when a file name does not match the required format rules."""

    error_code: ClassVar[str] = "FILE_STATE_NAME_FORMAT_ERROR"
    file_name: str | None = public_field(
        default=None, description="Offending file name"
    )
