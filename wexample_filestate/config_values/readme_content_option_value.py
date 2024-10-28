from typing import Any

from wexample_filestate.const.types_state_items import TargetFileOrDirectory
from wexample_filestate.config_values.aggregated_templates_config_value import AggregatedTemplatesConfigValue


class ReadmeContentConfigValue(AggregatedTemplatesConfigValue):
    @staticmethod
    def get_value_type() -> type:
        return Any

    def render(self, target: TargetFileOrDirectory, current_value: str) -> str:
        self.templates = [
            f'# {target.parent.get_name()}',
            '## Introduction',
            '## License'
        ]

        return super().render(target, current_value)
