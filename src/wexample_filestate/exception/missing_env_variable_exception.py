from __future__ import annotations

from typing import ClassVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.exception.abstract_file_state_exception import (
    AbstractFileStateException,
)


@base_class
class MissingEnvVariableException(AbstractFileStateException):
    """Exception raised when a required environment variable is missing."""

    error_code: ClassVar[str] = "FILE_STATE_MISSING_ENV_VARIABLE"

    env_key: str | None = public_field(
        default=None, description="Name of the missing environment variable"
    )
