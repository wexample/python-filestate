from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig
    from wexample_filestate.config_value.readme_content_config_value import (
        ReadmeContentConfigValue,
    )


@base_class
class WithReadmeWorkdirMixin(BaseClass):
    README_FILENAME: ClassVar[str] = "README.md"

    def append_readme(self, config: DictConfig | None = None) -> DictConfig:
        from wexample_filestate.option.text_filter_option import (
            TextFilterOption,
        )
        from wexample_filestate.config_value.readme_content_config_value import (
            ReadmeContentConfigValue,
        )
        from wexample_filestate.const.disk import DiskItemType

        config.get("children").append(
            {
                "name": self.README_FILENAME,
                "type": DiskItemType.FILE,
                "should_exist": True,
                "content": self._get_readme_content(),
                "default_content": ReadmeContentConfigValue(
                    templates=[], parameters={}
                ),
                "text_filter": [TextFilterOption.OPTION_NAME_ENSURE_NEWLINE],
            }
        )

        return config

    def _get_readme_content(self) -> ReadmeContentConfigValue | None:
        from wexample_filestate.config_value.readme_content_config_value import (
            ReadmeContentConfigValue,
        )

        return ReadmeContentConfigValue(templates=[], parameters={})
