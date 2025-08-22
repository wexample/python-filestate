from __future__ import annotations

import os
from typing import TYPE_CHECKING

from wexample_filestate.config_option.content_config_option import ContentConfigOption
from wexample_filestate.config_option.should_contain_lines_config_option import (
    ShouldContainLinesConfigOption,
)
from wexample_filestate.enum.scopes import Scope
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.operation.mixin.file_manipulation_operation_mixin import (
    FileManipulationOperationMixin,
)
from wexample_helpers.helpers.file import file_read

if TYPE_CHECKING:
    from wexample_config.config_option.abstract_config_option import (
        AbstractConfigOption,
    )
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class FileWriteOperation(FileManipulationOperationMixin, AbstractOperation):

    @classmethod
    def get_scope(cls) -> Scope:
        return Scope.CONTENT

    @classmethod
    def applicable_option(
        cls, target: TargetFileOrDirectoryType, option: AbstractConfigOption
    ) -> bool:
        if isinstance(option, ContentConfigOption):
            current_content = target.get_local_file().read()
            new_content = target.get_option_value(ContentConfigOption).get_str()
            return current_content != new_content

        if isinstance(option, ShouldContainLinesConfigOption):
            # Use the same representation as describe_before(): a list of strings
            required_lines = target.get_option_value(
                ShouldContainLinesConfigOption
            ).get_list()
            if not target.get_local_file().path.exists():
                return True
            current_content = target.get_local_file().read()
            current_lines = current_content.splitlines()
            return any(line not in current_lines for line in required_lines)

        return False

    def describe_before(self) -> str:
        content_option = self.target.get_option(ContentConfigOption)
        should_contain_lines_option = self.target.get_option(
            ShouldContainLinesConfigOption
        )

        if content_option is not None:
            return "The file content does not match the configured content and will be rewritten."

        if should_contain_lines_option is not None:
            current_content = (
                self.target.get_local_file().read()
                if self.target.get_local_file().path.exists()
                else ""
            )
            current_lines = current_content.splitlines()
            required_lines = self.target.get_option_value(
                ShouldContainLinesConfigOption
            ).get_list()
            missing = [l for l in required_lines if l not in current_lines]
            if missing:
                return f"The file is missing required lines which will be appended: {missing}."
            return "The file already contains all required lines."

        return "The file content may need to be regenerated based on configuration."

    def describe_after(self) -> str:
        if self.target.get_option(ContentConfigOption) is not None:
            return "The file content has been rewritten to exactly match the configured content."

        if self.target.get_option(ShouldContainLinesConfigOption) is not None:
            return "All required lines are now present in the file."

        return "The file content has been updated according to configuration."

    def description(self) -> str:
        return "Write or update file content to comply with configured content or required lines."

    def apply(self) -> None:
        content_option = self.target.get_option(ContentConfigOption)
        should_contain_lines_option = self.target.get_option(
            ShouldContainLinesConfigOption
        )
        updated_content = None

        if content_option is not None:
            updated_content = self.target.get_option_value(
                ContentConfigOption
            ).get_str()

        if should_contain_lines_option is not None:
            from wexample_helpers.helpers.string import string_append_missing_lines

            # Initialize content from existing file or empty string if file doesn't exist
            if updated_content is None:
                updated_content = (
                    file_read(self.target.get_resolved())
                    if os.path.exists(self.target.get_resolved())
                    else ""
                )

            updated_content = string_append_missing_lines(
                lines=self.target.get_option_value(
                    ShouldContainLinesConfigOption
                ).get_list(),
                content=updated_content,
            )

        if updated_content is not None:
            self._target_file_write(content=updated_content)

    def undo(self) -> None:
        self._restore_target_file()
