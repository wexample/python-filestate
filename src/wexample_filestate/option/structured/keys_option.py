from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_filestate.enum.scopes import Scope
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.operation.abstract_operation import AbstractOperation


@base_class
class StructuredKeysOption(OptionMixin, AbstractConfigOption):
    @classmethod
    def get_scopes(cls) -> list[Scope]:
        return [Scope.CONTENT]

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return dict

    def applicable_on_directory(self) -> bool:
        return False

    def applicable_on_missing(self) -> bool:
        return False

    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        from wexample_filestate.item.file.structured_content_file import (
            StructuredContentFile,
        )
        from wexample_filestate.operation.file_write_operation import FileWriteOperation

        if not isinstance(target, StructuredContentFile):
            return None

        expected = self.get_value().get_dict_or_empty()
        if not expected:
            return None

        cfg = target.read_config()
        mismatches: list[tuple[str, Any]] = []

        for key_path, expected_value in expected.items():
            current = cfg.search(key_path)
            if current.raw != expected_value:
                mismatches.append((key_path, expected_value))

        if not mismatches:
            return None

        for key_path, value in mismatches:
            cfg.set_by_path(key_path, value)

        return FileWriteOperation(
            option=self,
            target=target,
            content=target.preview_write_config(cfg),
            description=f"Set {len(mismatches)} key(s): {', '.join(k for k, _ in mismatches)}",
        )
