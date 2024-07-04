from __future__ import annotations

from git import Repo

from wexample_filestate.operation.abstract_git_operation import AbstractGitOperation
from wexample_helpers.const.globals import GIT_DIR_NAME
from wexample_helpers.helpers.git_helper import git_is_init


class GitInitOperation(AbstractGitOperation):
    _original_path_str: str
    _has_initialized_git: bool = False

    def describe_before(self) -> str:
        return 'No initialized .git directory'

    def describe_after(self) -> str:
        return 'Initialized .git directory'

    def description(self) -> str:
        return 'Initialize .git directory'

    def apply(self) -> None:
        path = self.get_target_file_path()
        self._has_initialized_git = True

        repo = Repo.init(path)
        repo.init()

    def undo(self) -> None:
        import shutil

        shutil.rmtree(self.get_target_file_path() + GIT_DIR_NAME)
