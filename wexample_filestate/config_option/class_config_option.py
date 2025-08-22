from __future__ import annotations

from typing import Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class ClassConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.item.item_target_file import ItemTargetFile

        return type[ItemTargetDirectory] | type[ItemTargetFile]
