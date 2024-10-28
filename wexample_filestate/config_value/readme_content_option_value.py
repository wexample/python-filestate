from typing import Any, TYPE_CHECKING

from wexample_filestate.config_value.aggregated_templates_config_value import AggregatedTemplatesConfigValue

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation


class ReadmeContentConfigValue(AggregatedTemplatesConfigValue):
    @staticmethod
    def get_value_type() -> type:
        return Any

    def render(self, operation: "AbstractOperation") -> str:
        self.templates = [
            f'# {target.parent.get_name()}',
            '## Introduction',
            '## License'
        ]

        return super().render(operation)
