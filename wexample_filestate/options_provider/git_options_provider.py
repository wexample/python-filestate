from typing import List, Type, TYPE_CHECKING

from wexample_filestate.options_provider.abstract_options_provider import AbstractOptionsProvider

if TYPE_CHECKING:
    from wexample_filestate.options.abstract_option import AbstractOption
    from wexample_filestate.operation.abstract_operation import AbstractOperation


class GitOptionsProvider(AbstractOptionsProvider):
    def get_options(self) -> List[Type["AbstractOption"]]:
        from wexample_filestate.options.git_option import GitOption

        return [
            GitOption
        ]

    def get_operations(self) -> List[Type["AbstractOperation"]]:
        from wexample_filestate.operation.git_init_operation import GitInitOperation
        from wexample_filestate.operation.git_remote_add_operation import GitRemoteAddOperation

        return [
            GitInitOperation,
            GitRemoteAddOperation
        ]
