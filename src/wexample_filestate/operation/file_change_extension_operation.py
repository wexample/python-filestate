from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.operation.mixin.file_manipulation_operation_mixin import (
    FileManipulationOperationMixin,
)

if TYPE_CHECKING:
    from wexample_config.config_option.abstract_config_option import (
        AbstractConfigOption,
    )
    from wexample_filestate.enum.scopes import Scope


class FileChangeExtensionOperation(FileManipulationOperationMixin, AbstractOperation):
    _original_extension: str | None = None

    @classmethod
    def get_scope(cls) -> Scope:
        from wexample_filestate.enum.scopes import Scope

        return Scope.NAME

    def applicable_for_option(self, option: AbstractConfigOption) -> bool:
        from wexample_filestate.option.should_have_extension_option import (
            ShouldHaveExtensionOption,
        )
        from wexample_filestate.item.item_source_file import ItemSourceFile

        if (
            self.target.source
            and self.target.is_file()
            and isinstance(option, ShouldHaveExtensionOption)
        ):
            assert isinstance(self.target.source, ItemSourceFile)
            if (
                self.target.source.get_local_file().get_extension()
                != option.get_value().get_str()
            ):
                return True
        return False

    def apply(self) -> None:
        from wexample_filestate.option.should_have_extension_option import (
            ShouldHaveExtensionOption,
        )

        self._original_extension = self.target.get_path().with_suffix("").name

        self.target.get_local_file().change_extension(
            self.target.get_option_value(ShouldHaveExtensionOption).get_str()
        )

    def describe_after(self) -> str:
        from wexample_filestate.option.should_have_extension_option import (
            ShouldHaveExtensionOption,
        )

        expected_ext = self.target.get_option_value(
            ShouldHaveExtensionOption
        ).get_str()
        path = self.target.get_path().with_suffix("").name
        return f"The file '{path}' now has the expected extension '.{expected_ext}'."

    def describe_before(self) -> str:
        from wexample_filestate.option.should_have_extension_option import (
            ShouldHaveExtensionOption,
        )

        current_ext = (
            self.target.get_source().get_local_file().get_extension()
            if self.target.get_source()
            else None
        )
        expected_ext = self.target.get_option_value(
            ShouldHaveExtensionOption
        ).get_str()
        path = self.target.get_path().name
        if current_ext is None:
            return f"The file '{path}' has no detectable extension but should have '.{expected_ext}'."
        return f"The file '{path}' has extension '.{current_ext}' but should be '.{expected_ext}'. Its extension will be corrected."

    def description(self) -> str:
        return "Ensure the file extension matches the configured requirement, correcting it when necessary."

    def undo(self) -> None:
        self.target.get_local_file().change_extension(self._original_extension)

        self._original_extension = None
