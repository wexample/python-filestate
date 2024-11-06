from typing import TYPE_CHECKING, List

from wexample_config.const.types import DictConfig
from wexample_filestate.config_option.abstract_children_manipulator_config_option import \
    AbstractChildrenManipulationConfigOption

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class ChildrenFileFactoryConfigOption(AbstractChildrenManipulationConfigOption):
    pattern: DictConfig

    def generate_children(self) -> List["TargetFileOrDirectoryType"]:
        from pathlib import Path
        config = self.pattern
        children = []
        directories = self._get_directories_filtered(
            base_path=self.get_parent_item().get_resolved(),
            recursive=config.get("recursive", False))

        for directory in directories:
            path = Path(directory)
            if self._path_match_patterns(path.name):
                children.append(
                    self._create_children_from_config(path, {
                        "name": config["name"],
                        "type": config["type"],
                        "should_exist": True
                    })
                )

        return children
