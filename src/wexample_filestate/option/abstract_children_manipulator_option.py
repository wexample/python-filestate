from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_config.config_option.abstract_nested_config_option import (
    AbstractNestedConfigOption,
)
from wexample_config.const.types import DictConfig
from wexample_filestate.config_option.mixin.item_config_option_mixin import (
    ItemTreeConfigOptionMixin,
)
from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_config.options_provider.abstract_options_provider import (
        AbstractOptionsProvider,
    )
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_helpers.const.types import PathOrString


@base_class
class AbstractChildrenManipulationOption(
    OptionMixin,
    ItemTreeConfigOptionMixin,
    AbstractNestedConfigOption,
):
    pattern: DictConfig = public_field(
        description="Pattern configuration used for children manipulation",
    )

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return DictConfig

    @abstract_method
    def generate_children(self) -> list[TargetFileOrDirectoryType]:
        pass

    def get_options_providers(self) -> list[type[AbstractOptionsProvider]]:
        from wexample_filestate.options_provider.default_options_provider import (
            DefaultOptionsProvider,
        )

        return [
            DefaultOptionsProvider,
        ]

    def _create_children_from_config(
        self, path: Path, config: dict
    ) -> TargetFileOrDirectoryType:
        import copy

        from wexample_filestate.option.children_option import (
            ChildrenOption,
        )

        item_config_copy = copy.deepcopy(config)

        if item_config_copy.get("name", None) is None:
            item_config_copy["name"] = path.name

        parent_children_config = cast(ChildrenOption, self.get_parent())

        return parent_children_config.create_child_item(
            child_config=item_config_copy,
        )

    def _get_directories_filtered(
        self, base_path: PathOrString, recursive: bool = False
    ) -> list[str]:
        from wexample_helpers.helpers.file import file_get_directories

        output = []
        directories = file_get_directories(path=base_path)

        for directory in directories:
            if self._path_match_patterns(directory):
                output.append(directory)

                if recursive is True:
                    output.extend(
                        self._get_directories_filtered(
                            base_path=directory, recursive=recursive
                        )
                    )

        return output

    def _path_match_patterns(self, path: str) -> bool:
        import re
        from pathlib import Path

        from wexample_filestate.option.name_pattern_option import (
            NamePatternOption,
        )

        config = self.pattern
        option_name = NamePatternOption.get_name()
        if config.get(option_name) is None:
            return True

        patterns = config[option_name]

        if isinstance(patterns, str):
            patterns = [patterns]

        for pattern_str in patterns:
            pattern = re.compile(pattern_str)
            if not pattern.match(Path(path).name):
                return False

        return True
