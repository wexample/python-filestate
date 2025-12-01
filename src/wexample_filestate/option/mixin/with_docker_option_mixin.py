from typing import TYPE_CHECKING

from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class WithDockerOptionMixin:

    def _ensure_docker_container(self) -> None:
        from wexample_helpers.helpers.shell import shell_run

        shell_run(
            cmd=[
                # TODO
                "docker",
                "ps"
            ],
            inherit_stdio=True
        )

    def _execute_in_docker(self, target: TargetFileOrDirectoryType, command: str):
        from wexample_helpers.helpers.shell import shell_run

        self._ensure_docker_container()

        shell_run(
            cmd=[
                "echo",
                command
            ],
            inherit_stdio=True
        )
