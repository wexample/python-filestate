from __future__ import annotations

from pydantic import BaseModel

from wexample_helpers.const.types import FileStringOrPath


class StateItemSourceMixin(BaseModel):
    path: FileStringOrPath
