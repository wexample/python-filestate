from typing import Optional

from pydantic import BaseModel

from wexample_filestate.const.types_state_items import TargetFileOrDirectory


class StringOptionValue(BaseModel):
    default_content: str = ''

    def render(self, target: TargetFileOrDirectory, current_value: Optional[str]) -> str:
        return current_value or self.default_content
