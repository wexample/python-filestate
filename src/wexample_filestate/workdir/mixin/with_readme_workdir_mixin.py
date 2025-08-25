from __future__ import annotations

from wexample_config.const.types import DictConfig
from wexample_filestate.config_option.text_filter_config_option import (
    TextFilterConfigOption,
)
from wexample_filestate.config_value.readme_content_config_value import (
    ReadmeContentConfigValue,
)
from wexample_filestate.const.disk import DiskItemType


class WithReadmeWorkdirMixin:
    def append_readme(self, config: DictConfig | None = None) -> DictConfig:
        config.get("children").append(
            {
                "name": "README.md",
                "type": DiskItemType.FILE,
                "should_exist": True,
                "default_content": ReadmeContentConfigValue(
                    templates=[], parameters={}
                ),
                "text_filter": [TextFilterConfigOption.OPTION_NAME_ENSURE_NEWLINE],
            }
        )

        return config
