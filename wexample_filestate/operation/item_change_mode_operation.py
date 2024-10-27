from __future__ import annotations
from typing import Optional
from wexample_filestate.operation.abstract_operation import AbstractOperation


class ItemChangeModeOperation(AbstractOperation):
    _original_octal_mode: Optional[str] = None
