from __future__ import annotations

from wexample_filestate.config_value.aggregated_templates_config_value import (
    AggregatedTemplatesConfigValue,
)
from wexample_helpers.decorator.base_class import base_class


@base_class
class ReadmeContentConfigValue(AggregatedTemplatesConfigValue):
    def get_templates(self) -> list[str] | None:
        return []
