import os
from typing import Any, cast, Union, Optional, List

from wexample_config.config_option.children_config_option import (
    ChildrenConfigOption as BaseChildrenConfigOption,
)
from wexample_config.const.types import DictConfig
from wexample_filestate.config_option.child_factory_config_option import ChildFactoryConfigOption
from wexample_filestate.config_option.mixin.item_config_option_mixin import ItemTreeConfigOptionMixin
from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class ChildrenConfigOption(ItemTreeConfigOptionMixin, BaseChildrenConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.config_option.child_factory_config_option import ChildFactoryConfigOption

        return list[Union[dict[str, Any], ChildFactoryConfigOption]]

    def get_parent(self) -> "TargetFileOrDirectoryType":
        assert self.parent is not None
        return cast("TargetFileOrDirectory", self.parent)

    def set_value(self, raw_value: Any):
        from wexample_config.config_option.abstract_config_option import (
            AbstractConfigOption,
        )

        # Ignore default children class set_value
        AbstractConfigOption.set_value(self, raw_value)

    def build_item_tree(self):
        super().build_item_tree()
        children = self.create_children_items()

        # Continue item tree.
        for child in children:
            child.build_item_tree()

    def create_children_items(self) -> List["TargetFileOrDirectoryType"]:
        children = []
        # Parent item should be a file or directory target.
        for child_config in self.get_value().get_list():
            if isinstance(child_config, ChildFactoryConfigOption):
                child = child_config
                # Parent has not been assigned before now.
                child.parent = self

                children.extend(child.generate_children())

            else:
                children.append(self.create_child_item(
                    child_config=child_config
                ))

        self.children = children
        return children

    def create_child_item(
        self,
        child_config: DictConfig,
        item_name: Optional[str] = None
    ) -> "TargetFileOrDirectoryType":
        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.helpers.config_helper import config_is_item_type
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.item.item_target_file import ItemTargetFile

        if "class" in child_config:
            class_name = child_config.get("class")

            if not issubclass(
                class_name, ItemTargetDirectory
            ) and not issubclass(
                child_config.get("class"), ItemTargetFile
            ):
                from wexample_filestate.exception.config import (
                    BadConfigurationClassTypeException,
                )

                raise BadConfigurationClassTypeException(
                    f"Class {child_config['class'].__name__} option "
                    f"should extend {ItemTargetDirectory.__name__} "
                    f"or {ItemTargetFile.__name__}"
                )

            child = class_name(
                # Name might be not mandatory when using custom class
                item_name=item_name or child_config.get("name", None),
                config=child_config,
                parent=self,
            )
        else:
            name = item_name or child_config.get("name", None)
            if name is None:
                from wexample_filestate.exception.config import MissingNameInConfigurationException
                raise MissingNameInConfigurationException(
                    "Name is missing in the child configuration."
                )

            is_file_type = config_is_item_type(child_config, DiskItemType.FILE)
            # The current item has a parent, so we can try to guess the file type.
            is_actual_file = isinstance(name, str) and os.path.isfile(
                os.path.join(self.get_parent_item().get_resolved(), name)
            )

            if is_file_type or is_actual_file:
                child = ItemTargetFile(
                    item_name=name,
                    parent=self,
                )
            else:
                child = ItemTargetDirectory(
                    item_name=name,
                    parent=self,
                )

        child.configure(child_config)
        return child

    def get_children(self) -> list[TargetFileOrDirectoryType]:
        return cast(list[TargetFileOrDirectoryType], self.children)
