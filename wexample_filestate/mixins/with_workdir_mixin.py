from typing import Optional, Type

from wexample_config.const.types import DictConfig
from wexample_filestate.file_state_manager import FileStateManager
from wexample_prompt.common.io_manager import IoManager


class WithWorkdirMixin:
    workdir: FileStateManager = None
    host_workdir: FileStateManager = None

    def _init_workdir(
            self,
            entrypoint_path: str,
            io_manager: IoManager,
            config: Optional[DictConfig] = None
    ) -> None:
        import os

        self.workdir = (self._get_workdir_state_manager_class()).create_from_path(
            path=entrypoint_path,
            config=config or {},
            io_manager=io_manager
        )

        # Ensure files state.
        self.workdir.apply()

        # The calling workdir may be in a virtual env host system.
        self.host_workdir = FileStateManager.create_from_path(
            path=os.getcwd(),
            io_manager=io_manager
        )

    def _get_workdir_state_manager_class(self) -> Type[FileStateManager]:
        return FileStateManager
