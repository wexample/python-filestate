import os
from typing import Any, Optional, cast, Union, Type

from wexample_config.config_option.children_config_option import (
    ChildrenConfigOption as BaseChildrenConfigOption,
)
from wexample_config.const.types import DictConfig
from wexample_filestate.const.types_state_items import TargetFileOrDirectory
from wexample_filestate.config_option.mixin.item_config_option_mixin import ItemTreeConfigOptionMixin
from wexample_filestate.item.file_state_item_directory_target import (
    FileStateItemDirectoryTarget,
)
from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget


class ChildrenConfigOption(BaseChildrenConfigOption):
    parent: Optional[TargetFileOrDirectory] = None
class ChildrenConfigOption(ItemTreeConfigOptionMixin, BaseChildrenConfigOption):

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.config_option.child_factory_config_option import ChildFactoryConfigOption

        return list[Union[dict[str, Any], ChildFactoryConfigOption]]

    def get_parent(self) -> "TargetFileOrDirectory":
        assert self.parent is not None
        return cast("TargetFileOrDirectory", self.parent)

    def set_value(self, raw_value: Any):
        from wexample_filestate.config_option.child_factory_config_option import ChildFactoryConfigOption

        from wexample_config.config_option.abstract_config_option import (
            AbstractConfigOption,
        )

        AbstractConfigOption.set_value(self, raw_value)

        # If child is not linked to any parent item.
        if not self.parent:
            return

        # Parent item should be a file or directory target.
        for child_config in raw_value:
            if isinstance(child_config, ChildFactoryConfigOption):
                child_config.parent = self
                child_config.generate_children()
            elif isinstance(child_config, dict):
                self.create_child_item(child_config=child_config)

    def create_child_item(self, child_config: DictConfig) -> None:
        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.helpers.config_helper import config_is_item_type

        item_name = child_config.get("name")

        if "class" in child_config:
            class_name = child_config.get("class")

            if not issubclass(
                class_name, FileStateItemDirectoryTarget
            ) and not issubclass(
                child_config.get("class"), FileStateItemFileTarget
            ):
                from wexample_filestate.exception.config import (
                    BadConfigurationClassTypeException,
                )

                raise BadConfigurationClassTypeException(
                    f"Class {child_config['class'].__name__} option "
                    f"should extend {FileStateItemDirectoryTarget.__name__} "
                    f"or {FileStateItemFileTarget.__name__}"
                )

            child = class_name(
                config=child_config,
                parent=self,
                parent_item=self.parent,
            )

        else:
            is_file_type = config_is_item_type(child_config, DiskItemType.FILE)
            is_actual_file = isinstance(item_name, str) and os.path.isfile(
                os.path.join(self.get_parent().get_resolved(), item_name)
            )

            if is_file_type or is_actual_file:
                child = FileStateItemFileTarget(
                    config=child_config,
                    parent=self,
                    parent_item=self.parent,
                )
            else:
                child = FileStateItemDirectoryTarget(
                    config=child_config,
                    parent=self,
                    parent_item=self.parent,
                )

        self.children.append(child)

    def get_children(self) -> list[TargetFileOrDirectory]:
        return cast(list[TargetFileOrDirectory], self.children)
