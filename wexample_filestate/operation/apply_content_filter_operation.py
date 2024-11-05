from __future__ import annotations

from typing import TYPE_CHECKING, cast

from wexample_config.config_value.config_value import ConfigValue
from wexample_filestate.config_option.content_filter_config_option import ContentFilterConfigOption
from wexample_filestate.operation.file_write_operation import FileWriteOperation
from wexample_helpers.helpers.file_helper import file_read

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class ApplyContentFilterOperation(FileWriteOperation):
    _original_path_str: str

    @staticmethod
    def applicable(
        target: "TargetFileOrDirectoryType"
    ) -> bool:
        from wexample_filestate.config_option.content_filter_config_option import (
            ContentFilterConfigOption,
        )
        if target.source and target.get_option(ContentFilterConfigOption) is not None:
            return True

        return False

    def describe_before(self) -> str:
        return "TO_FILTER"

    def describe_after(self) -> str:
        return "FILTERED"

    def description(self) -> str:
        return "Apply given filters on content"

    def apply(self) -> None:
        filters = cast(ContentFilterConfigOption, self.target.get_option(ContentFilterConfigOption)).get_filters()

        self._target_file_write(
            content=ConfigValue.apply_filters(
                content=file_read(self._get_target_file_path(target=self.target)),
                filters=filters,
            )
        )
