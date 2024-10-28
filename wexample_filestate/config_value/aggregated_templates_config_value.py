import os
from typing import Dict, Optional, List, Any, TYPE_CHECKING

from wexample_filestate.config_value.item_config_value import ItemConfigValue
from wexample_helpers.const.types import BasicValue

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation


class AggregatedTemplatesConfigValue(ItemConfigValue):
    raw: Any = None
    templates: Optional[List[str]] = []
    parameters: Optional[Dict[str, BasicValue]] = {}

    def render(self, operation: "AbstractOperation") -> str:
        output = []

        for template_content in self.templates:
            output.append(template_content.format(self.parameters))

        output_str = os.linesep.join(output)
        self.set_str(output_str)

        return output_str
