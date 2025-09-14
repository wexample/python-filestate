from __future__ import annotations

import os
from typing import TYPE_CHECKING, cast

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.operation.mixin.file_manipulation_operation_mixin import (
    FileManipulationOperationMixin,
)

if TYPE_CHECKING:
    from wexample_config.config_option.abstract_config_option import (
        AbstractConfigOption,
    )
    from wexample_filestate.enum.scopes import Scope


class FileCreateOperation(FileManipulationOperationMixin, AbstractOperation):
    @classmethod
    def get_scope(cls) -> Scope:
        from wexample_filestate.enum.scopes import Scope

        return Scope.LOCATION

    def applicable_for_option(self, option: AbstractConfigOption) -> bool:
        return (
            self.target.source is None
            and FileManipulationOperationMixin.option_should_exist_is_true(self.target)
        )

    def apply(self) -> None:
        from wexample_filestate.option.default_content_option import (
            DefaultContentOption,
        )

        self._original_path = self.target.get_path()

        if self.target.is_file():
            local_file = self.target.get_local_file()

            default_content = cast(
                DefaultContentOption,
                self.target.get_option(DefaultContentOption),
            )

            if default_content:
                default_content_option = self.target.get_option_value(
                    DefaultContentOption
                )

                if default_content_option:
                    local_file.write(default_content_option.get_str())
                else:
                    local_file.touch()
            else:
                local_file.touch()

        elif self.target.is_directory():
            os.mkdir(self._original_path)

    def describe_after(self) -> str:
        return f"The file or directory has been created."

    def describe_before(self) -> str:
        return f"The file or directory does not exists on the system."

    def description(self) -> str:
        return "Create missing file"

    def undo(self) -> None:
        if self.target.is_file():
            os.remove(self._original_path)
        elif self.target.is_directory():
            # Do not remove recursively, as for now it only can be created empty with mkdir.
            os.rmdir(self._original_path)
