import os
from typing import Optional, TYPE_CHECKING, List, Type
from pydantic import BaseModel
from wexample_filestate.const.disk import DiskItemType
from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget

if TYPE_CHECKING:
    from wexample_filestate.item.abstract_state_item import AbstractStateItem


class ChildConfig(BaseModel):
    config: Optional[dict] = None

    def parse_config(self, target) -> List["AbstractStateItem"]:
        base_path = target.get_resolved()
        item_name = self.config.get("name")
        item_type = self.config.get("type")
        is_file_type = item_type == DiskItemType.FILE or item_type == DiskItemType.FILE.value
        is_actual_file = isinstance(item_name, str) and os.path.isfile(os.path.join(base_path, item_name))

        if "class" in self.config:
            if not issubclass(self.config.get("class"), FileStateItemDirectoryTarget):
                from wexample_filestate.exception.config import BadConfigurationClassTypeException

                raise BadConfigurationClassTypeException(
                    f"Class {self.config['class'].__name__} option should extend {FileStateItemDirectoryTarget.__name__}")

            return [self.config["class"](base_path=base_path, config=self.config, parent=target)]

        if is_file_type or is_actual_file:
            state_item = FileStateItemFileTarget(base_path=base_path, config=self.config, parent=self)
        else:
            state_item = FileStateItemDirectoryTarget(base_path=base_path, config=self.config, parent=self)

        return [state_item]
