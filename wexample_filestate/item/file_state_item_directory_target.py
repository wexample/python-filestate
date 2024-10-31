from __future__ import annotations

from typing import Optional, cast, TYPE_CHECKING, List

from wexample_config.const.types import DictConfig
from wexample_filestate.item.file_state_item_directory import \
    FileStateItemDirectory
from wexample_filestate.item.mixins.state_item_target_mixin import \
    StateItemTargetMixin
from wexample_helpers.const.types import FileStringOrPath
from wexample_helpers.helpers.directory_helper import (
    directory_get_base_name, directory_get_parent_path)

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectory


class FileStateItemDirectoryTarget(StateItemTargetMixin, FileStateItemDirectory):
    def __init__(self, config: DictConfig, **data):
        StateItemTargetMixin.__init__(self, config=config, **data)

    def configure_from_file(self, path: FileStringOrPath):
        from wexample_helpers_yaml.helpers.yaml_helpers import yaml_read

        if yaml_read is not None:
            self.set_value(raw_value=yaml_read(str(path)))

    def get_children_list(self) -> list[TargetFileOrDirectory]:
        from wexample_filestate.config_option.children_config_option import ChildrenConfigOption
        from wexample_filestate.const.types_state_items import TargetFileOrDirectory

        option = cast(ChildrenConfigOption, self.get_option(ChildrenConfigOption))
        if option is not None:
            return cast(List[TargetFileOrDirectory], option.children)

        return []

    def find_by_name_recursive(self, name: str) -> Optional["TargetFileOrDirectory"]:
        found = self.find_by_name(name)
        if found:
            return found

        for child in self.get_children_list():
            result = child.find_by_name_recursive(name)
            if result:
                return result

        return None

    def find_by_name(self, name: str) -> Optional["TargetFileOrDirectory"]:
        for child in self.get_children_list():
            if child.get_item_name() == name:
                return child

        return None

    def find_by_name_or_fail(self, name: str) -> "TargetFileOrDirectory":
        child = self.find_by_name(name)
        if child is None:
            from wexample_filestate.exception.item import \
                ChildNotFoundException
            raise ChildNotFoundException(f'Child not found: {name}')

        return child

    @classmethod
    def create_from_path(
        cls,
        path: str,
        config: Optional[DictConfig] = None,
    ) -> FileStateItemDirectoryTarget:
        config = config or {}

        config["name"] = directory_get_base_name(path)
        return cls(
            config=config,
            base_path=directory_get_parent_path(path),
        )
