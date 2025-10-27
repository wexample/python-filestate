from __future__ import annotations

from typing import Any, cast

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_filestate.option.mixin.with_current_content_option_mixin import WithCurrentContentOptionMixin
from wexample_helpers.decorator.base_class import base_class


@base_class
class ClassOption(OptionMixin, WithCurrentContentOptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.item.item_target_file import ItemTargetFile

        return type[ItemTargetDirectory] | type[ItemTargetFile]

    def create_required_operation(
            self, target: TargetFileOrDirectoryType
    ) -> AbstractOperation | None:
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.item.item_target_file import ItemTargetFile

        class_definition = cast(type[ItemTargetDirectory] | type[ItemTargetFile], self.value)
        item = class_definition.create_from_path(target.get_path())

        return self._create_write_operation_if_content_changed(
            target=target,
            target_content=item.preview_write()
        )

    def get_description(self) -> str:
        return "Define a class as a file or directory configuration manager"
