from __future__ import annotations

from typing import TYPE_CHECKING, Union, Optional, List, Type

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_filestate.config_option.text_filter_config_option import TextFilterConfigOption
from wexample_filestate.enum.scopes import Scope
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.operation.mixin.file_manipulation_operation_mixin import (
    FileManipulationOperationMixin,
)

if TYPE_CHECKING:
    from wexample_filestate.item.item_target_directory import ItemTargetDirectory
    from wexample_filestate.item.item_target_file import ItemTargetFile


class ContentTrimOperation(FileManipulationOperationMixin, AbstractOperation):
    _original_extension: Optional[str] = None

    @classmethod
    def get_scope(cls) -> Scope:
        return Scope.NAME

    def dependencies(self) -> List[Type["AbstractOperation"]]:
        from wexample_filestate.operation.file_create_operation import FileCreateOperation

        return [
            FileCreateOperation
        ]

    @staticmethod
    def applicable_option(
            target: Union["ItemTargetDirectory", "ItemTargetFile"],
            option: "AbstractConfigOption"
    ) -> bool:
        from wexample_filestate.config_option.text_filter_config_option import TextFilterConfigOption

        if target.is_file() and target.get_local_file().path.exists() and isinstance(option, TextFilterConfigOption):
            if option.get_value().has_item_in_list("trim"):
                content = target.get_local_file().read()
                char = option.get_trimmed_char()
                return content.startswith(char) or content.endswith(char)
        return False

    def _get_trimmed_char(self) -> str:
        return self.target.get_option(TextFilterConfigOption).get_trimmed_char()

    def describe_before(self) -> str:
        return f"The file contains the leading or the trailing char {repr(self._get_trimmed_char())} that should be trimmed."

    def describe_after(self) -> str:
        return f"The file content has been trimmed from the char {repr(self._get_trimmed_char())}."

    def description(self) -> str:
        return "Trim the file content according the given char."

    def apply(self) -> None:
        self._target_file_write(
            content=self.target.get_local_file().read().strip(
                self._get_trimmed_char()
            )
        )

    def undo(self) -> None:
        self._restore_target_file()
