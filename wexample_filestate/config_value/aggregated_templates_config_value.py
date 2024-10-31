import os
from types import UnionType
from typing import Dict, Optional, List, Any, Type
from wexample_filestate.config_value.item_config_value import ItemConfigValue
from wexample_helpers.const.types import BasicValue


class AggregatedTemplatesConfigValue(ItemConfigValue):
    raw: Any = None
    templates: Optional[List[str]] = []
    parameters: Optional[Dict[str, BasicValue]] = {}

    @staticmethod
    def get_value_allowed_type() -> Type | UnionType:
        return Any

    def render(self) -> str:
        output = []

        for template_content in self.templates:
            output.append(template_content.format(self.parameters))

        output_str = os.linesep.join(output)
        self.set_str(output_str)

        return output_str
