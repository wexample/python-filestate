from __future__ import annotations

import os
from typing import TYPE_CHECKING

from wexample_filestate.config_option.content_config_option import ContentConfigOption
from wexample_filestate.config_option.should_contain_lines_config_option import (
    ShouldContainLinesConfigOption,
)
from wexample_filestate.config_option.should_not_contain_lines_config_option import (
    ShouldNotContainLinesConfigOption,
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

    # ----------------------------
    # Internal helpers (factorized)
    # ----------------------------
    @staticmethod
    def _get_current_content_from_target(target: TargetFileOrDirectoryType) -> str:
        local_file = target.get_local_file()
        return local_file.read() if local_file.path.exists() else ""

    @staticmethod
    def _get_current_lines_from_target(
        target: TargetFileOrDirectoryType,
    ) -> list[str]:
        return FileWriteOperation._get_current_content_from_target(target).splitlines()

    @staticmethod
    def _join_with_original_newline(lines: list[str], original: str) -> str:
        """Join lines using \n and preserve a trailing newline if present in original."""
        trailing_newline = original.endswith("\n")
        updated = "\n".join(lines)
        if trailing_newline and (updated or original.splitlines()):
            updated += "\n"
        return updated

    @classmethod
    def applicable_option(
        cls, target: TargetFileOrDirectoryType, option: AbstractConfigOption
    ) -> bool:
        if isinstance(option, ContentConfigOption):
            current_content = cls._get_current_content_from_target(target)
            new_content = target.get_option_value(ContentConfigOption).get_str()
            return current_content != new_content

        if isinstance(option, ShouldContainLinesConfigOption):
            # Use the same representation as describe_before(): a list of strings
            required_lines = target.get_option_value(
                ShouldContainLinesConfigOption
            ).get_list()
            if not target.get_local_file().path.exists():
                return True
            current_lines = cls._get_current_lines_from_target(target)
            return any(line not in current_lines for line in required_lines)

        if isinstance(option, ShouldNotContainLinesConfigOption):
            # If file does not exist, there's nothing to remove yet, so not applicable.
            if not target.get_local_file().path.exists():
                return False
            forbidden_lines = target.get_option_value(
                ShouldNotContainLinesConfigOption
            ).get_list()
            current_lines = cls._get_current_lines_from_target(target)
            return any(line in current_lines for line in forbidden_lines)

        return False

    def describe_before(self) -> str:
        content_option = self.target.get_option(ContentConfigOption)
        should_contain_lines_option = self.target.get_option(
            ShouldContainLinesConfigOption
        )
        should_not_contain_lines_option = self.target.get_option(
            ShouldNotContainLinesConfigOption
        )

        if content_option is not None:
            return "The file content does not match the configured content and will be rewritten."

        if should_contain_lines_option is not None:
            current_lines = self._get_current_lines_from_target(self.target)
            required_lines = self.target.get_option_value(
                ShouldContainLinesConfigOption
            ).get_list()
            missing = [l for l in required_lines if l not in current_lines]
            if missing:
                return f"The file is missing required lines which will be appended: {missing}."
            return "The file already contains all required lines."

        if should_not_contain_lines_option is not None:
            current_lines = self._get_current_lines_from_target(self.target)
            forbidden_lines = self.target.get_option_value(
                ShouldNotContainLinesConfigOption
            ).get_list()
            present = [l for l in forbidden_lines if l in current_lines]
            if present:
                return f"The file contains forbidden lines which will be removed: {present}."
            return "The file does not contain any forbidden lines."

        return "The file content may need to be regenerated based on configuration."

    def describe_after(self) -> str:
        if self.target.get_option(ContentConfigOption) is not None:
            return "The file content has been rewritten to exactly match the configured content."

        if self.target.get_option(ShouldContainLinesConfigOption) is not None:
            return "All required lines are now present in the file."

        if self.target.get_option(ShouldNotContainLinesConfigOption) is not None:
            return "All forbidden lines have been removed from the file."

        return "The file content has been updated according to configuration."

    def description(self) -> str:
        return (
            "Write or update file content to comply with configured content, enforce required lines, "
            "and remove forbidden lines."
        )

    def apply(self) -> None:
        content_option = self.target.get_option(ContentConfigOption)
        should_contain_lines_option = self.target.get_option(
            ShouldContainLinesConfigOption
        )
        should_not_contain_lines_option = self.target.get_option(
            ShouldNotContainLinesConfigOption
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

        if should_not_contain_lines_option is not None:
            # Initialize content if not set yet
            if updated_content is None:
                updated_content = self._get_current_content_from_target(self.target)

            # Remove any line that exactly matches one of the forbidden lines
            forbidden = set(
                self.target.get_option_value(
                    ShouldNotContainLinesConfigOption
                ).get_list()
            )
            original = updated_content
            lines = original.splitlines()
            kept_lines = [l for l in lines if l not in forbidden]

            # Preserve trailing newline if present in original content
            updated_content = self._join_with_original_newline(kept_lines, original)

        if updated_content is not None:
            self._target_file_write(content=updated_content)

    def undo(self) -> None:
        self._restore_target_file()
