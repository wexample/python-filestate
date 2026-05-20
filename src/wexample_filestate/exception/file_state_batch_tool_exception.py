from __future__ import annotations

from wexample_filestate.exception.abstract_file_state_exception import (
    AbstractFileStateException,
)


class FileStateBatchToolException(AbstractFileStateException):
    """Raised when a batch tool (e.g. PHP-CS-Fixer, Biome) exits non-zero."""

    error_code: str = "FILE_STATE_BATCH_TOOL_ERROR"
