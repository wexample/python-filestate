from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from wexample_filestate.file_state_manager import FileStateManager


class AbstractFileStateManagerChild(BaseModel, ABC):
    state_manager: "FileStateManager"
