from __future__ import annotations

from abc import abstractmethod

from wexample_filestate.file_state_manager_child import AbstractFileStateManagerChild


class AbstractStateItem(AbstractFileStateManagerChild):
    def get_resolved(self):
        return self.path.resolve()

    @abstractmethod
    def is_file(self) -> bool:
        pass

    @abstractmethod
    def is_directory(self) -> bool:
        pass
