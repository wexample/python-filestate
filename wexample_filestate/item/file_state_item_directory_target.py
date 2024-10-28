from __future__ import annotations

from typing import Optional, List, cast, TYPE_CHECKING, Union
from pydantic import Field
from wexample_config.const.types import DictConfig
from wexample_filestate.item.abstract_state_item import AbstractStateItem
from wexample_filestate.item.file_state_item_directory import FileStateItemDirectory
from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
from wexample_filestate.item.mixins.state_item_target_mixin import StateItemTargetMixin
from wexample_prompt.io_manager import IOManager
from wexample_filestate.result.abstract_result import AbstractResult

if TYPE_CHECKING:
    from wexample_filestate.result.file_state_dry_run_result import FileStateDryRunResult


class FileStateItemDirectoryTarget(FileStateItemDirectory, StateItemTargetMixin):
    children: List[Union[AbstractStateItem, FileStateItemDirectoryTarget, FileStateItemFileTarget]] = []
    io: IOManager = Field(
        default_factory=IOManager,
        description="Handles output to print, allow to share it if defined in a parent context")
    last_result: Optional[AbstractResult] = None

    def configure(self, config: Optional[DictConfig]) -> None:
        from wexample_filestate.utils.child_config import ChildConfig
        super().configure(config)

        if "children" in config:
            import copy

            for item_config in config["children"]:
                if isinstance(item_config, ChildConfig):
                    child_config = item_config
                else:
                    child_config = ChildConfig(config=copy.deepcopy(item_config))

                self.children.extend(
                    child_config.parse_config(
                        target=self,
                    )
                )

    def build_operations(self, result: AbstractResult):
        super().build_operations(result)
        from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget

        for item in self.children:
            cast(Union[FileStateItemDirectoryTarget, FileStateItemFileTarget], item).build_operations(result)

    def find_by_name(self, name: str) -> Optional["AbstractStateItem"]:
        for child in self.children:
            if child.get_name() == name:
                return child

        return None

    def run(self, result: AbstractResult) -> "AbstractResult":
        self.build_operations(result)
        self.last_result = result

        return self.last_result

    def dry_run(self) -> "FileStateDryRunResult":
        from wexample_filestate.result.file_state_dry_run_result import FileStateDryRunResult

        return cast(FileStateDryRunResult, self.run(FileStateDryRunResult(state_manager=self)))

    @classmethod
    def create_from_path(
        cls,
        path: str,
        config: Optional[DictConfig] = None,
        io: Optional[IOManager] = None
    ) -> FileStateItemDirectoryTarget:
        import os
        from wexample_helpers.helpers.directory_helper import directory_get_base_name, directory_get_parent_path

        config = config or {}

        # If path is a file, ignore file name a keep parent directory.
        if os.path.isfile(path):
            path = os.path.dirname(path)

        config["name"] = directory_get_base_name(path)

        return cls(
            config=config,
            base_path=directory_get_parent_path(path),
            io=io or IOManager(),
        )
