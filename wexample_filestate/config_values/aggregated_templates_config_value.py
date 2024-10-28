import os
from typing import Dict, Optional, List, Any

from wexample_filestate.const.types_state_items import TargetFileOrDirectory
from wexample_filestate.config_values.content_config_value import ContentConfigValue
from wexample_helpers.const.types import BasicValue


class AggregatedTemplatesConfigValue(ContentConfigValue):
    raw: Any = None
    templates: List[str]
    parameters: Dict[str, BasicValue]

    def __init__(self, templates: List[str], parameters: Optional[Dict[str, BasicValue]]):
        super().__init__(templates=templates, parameters=parameters or {})

    def render(self, target: TargetFileOrDirectory, current_value: str) -> str:
        output = []

        for template_content in self.templates:
            output.append(template_content.format(self.parameters))
        return os.linesep.join(output)

    def get_str(self, type_check: bool = True) -> str:
        return "yop"
