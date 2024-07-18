import os
from typing import Dict, Optional, List

from wexample_filestate.const.types_state_items import TargetFileOrDirectory
from wexample_filestate.options_values.content_option_value import ContentOptionValue
from wexample_helpers.const.types import BasicValue


class AggregatedTemplatesOptionValue(ContentOptionValue):
    templates: List[str]
    parameters: Dict[str, BasicValue]

    def __init__(self, templates: List[str], parameters: Optional[Dict[str, BasicValue]]):
        super().__init__(templates=templates, parameters=parameters or {})

    def render(self, target: TargetFileOrDirectory, current_value: str) -> str:
        output = []

        for template_content in self.templates:
            output.append(template_content.format(self.parameters))
        return os.linesep.join(output)
