from __future__ import annotations

from wexample_filestate.exception.abstract_file_state_exception import (
    AbstractFileStateException,
)


class FileStatePermissionException(AbstractFileStateException):
    """Raised when an operation is denied due to filesystem permissions."""

    error_code: str = "FILE_STATE_PERMISSION_ERROR"
