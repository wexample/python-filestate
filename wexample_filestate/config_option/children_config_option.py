import os
from typing import Any

from wexample_config.config_option.children_config_option import ChildrenConfigOption as BaseChildrenConfigOption
from wexample_filestate.const.disk import DiskItemType
from wexample_filestate.helpers.config_helper import config_is_item_type
from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget


class ChildrenConfigOption(BaseChildrenConfigOption):

    def set_value(self, raw_value: Any):
        super().set_value(raw_value)

        base_path = self.parent.get_resolved()
        for child_config in raw_value:
            item_name = child_config.get("name")

            if "class" in child_config:
                class_name = child_config.get("class")

                if not issubclass(class_name, FileStateItemDirectoryTarget) and not issubclass(
                    child_config.get("class"), FileStateItemFileTarget):
                    from wexample_filestate.exception.config import BadConfigurationClassTypeException

                    raise BadConfigurationClassTypeException(
                        f"Class {child_config['class'].__name__} option "
                        f"should extend {FileStateItemDirectoryTarget.__name__} "
                        f"or {FileStateItemFileTarget.__name__}")

                class_name(
                    base_path=base_path,
                    config=child_config,
                    parent=self,
                )

            else:
                is_file_type = config_is_item_type(child_config, DiskItemType.FILE)
                is_actual_file = isinstance(item_name, str) and os.path.isfile(os.path.join(base_path, item_name))

                if is_file_type or is_actual_file:
                    FileStateItemFileTarget(
                        base_path=base_path,
                        config=child_config,
                        parent=self,
                    )
                else:
                    FileStateItemDirectoryTarget(
                        base_path=base_path,
                        config=child_config,
                        parent=self,
                    )
