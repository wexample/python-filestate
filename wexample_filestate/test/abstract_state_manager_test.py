from abc import ABC

from wexample_filestate.file_state_manager import FileStateManager


class AbstractStateManagerTest(ABC):
    state_manager: "FileStateManager"

    def setup_method(self) -> None:
        from wexample_filestate.file_state_manager import FileStateManager

        self.state_manager = FileStateManager.create_from_path()
