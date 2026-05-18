from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig
    from wexample_prompt.common.io_manager import IoManager

    from wexample_filestate.utils.file_state_manager import FileStateManager


@base_class
class WithWorkdirMixin(BaseClass):
    _host_workdir: FileStateManager | None = private_field(
        default=None,
        description="Internal file state manager for the host workdir",
    )
    _workdir: FileStateManager | None = private_field(
        default=None,
        description="Internal file state manager for the current working directory",
    )

    def __init__(self, *args, **kwargs) -> None:
        # Forward all arguments to parent class
        super().__init__(*args, **kwargs)

    @property
    def host_workdir(self) -> FileStateManager | None:
        return self._host_workdir

    @host_workdir.setter
    def host_workdir(self, value: FileStateManager | None) -> None:
        self._host_workdir = value

    @property
    def workdir(self) -> FileStateManager | None:
        return self._workdir

    @workdir.setter
    def workdir(self, value: FileStateManager | None) -> None:
        self._workdir = value

    def _create_workdir_state_manager(
        self,
        entrypoint_path: str,
        io: IoManager,
        config: DictConfig | None = None,
        configure: bool = True,
    ) -> FileStateManager:
        return self._get_workdir_state_manager_class().create_from_path(
            path=entrypoint_path,
            config=config or {},
            io=io,
            configure=configure,
        )

    def _get_workdir_state_manager_class(
        self,
    ) -> type[FileStateManager]:
        from wexample_filestate.utils.file_state_manager import FileStateManager

        return FileStateManager

    def _init_workdir(
        self,
        entrypoint_path: str,
        io: IoManager,
        config: DictConfig | None = None,
    ) -> None:
        import os

        from wexample_filestate.utils.file_state_manager import FileStateManager

        # Defer expensive option-tree construction (135ms+ for WexWorkdir).
        # Call self.workdir.configure(config) before operations that need shortcuts
        # or option lookups (apply, dry_run, find_by_path, get_option, get_shortcut).
        self.workdir = self._create_workdir_state_manager(
            entrypoint_path=entrypoint_path,
            io=io,
            config=config,
            configure=False,
        )

        # The calling workdir may be in a virtual env host system.
        self.host_workdir = FileStateManager.create_from_path(path=os.getcwd(), io=io)

    def _rebuild_workdir_content(self) -> None:
        from wexample_filestate.enum.scopes import Scope

        self.workdir.apply(
            scopes={
                Scope.CONTENT,
            }
        )
