from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.enum.scopes import Scope
from wexample_filestate.option.mixin.option_mixin import OptionMixin

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.operation.abstract_operation import AbstractOperation


def _get_by_path(data: Any, path: str) -> Any:
    current = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _set_by_path(data: Any, path: str, value: Any) -> None:
    parts = path.split(".")
    current = data
    for part in parts[:-1]:
        if part not in current or not isinstance(current[part], dict):
            current[part] = {}
        current = current[part]
    current[parts[-1]] = value


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

        # Operate directly on the parsed structure (ruamel CommentedMap for YAML)
        # to preserve comments, anchors and custom tags. Refuse to operate if
        # parsing fails — better skip than truncate the file.
        try:
            parsed = target.read_parsed(strict=True)
        except Exception:
            return None

        if not isinstance(parsed, dict):
            return None

        mismatches: list[tuple[str, Any]] = []
        for key_path, value in expected.items():
            if callable(value):
                value = value(target)
            elif hasattr(value, "raw") and callable(value.raw):
                value = value.raw(target)
            if _get_by_path(parsed, key_path) != value:
                mismatches.append((key_path, value))

        if not mismatches:
            return None

        # Apply changes in place on the parsed structure (preserves metadata).
        for key_path, value in mismatches:
            _set_by_path(parsed, key_path, value)

        return FileWriteOperation(
            option=self,
            target=target,
            content=target.dumps(parsed),
            description=f"Set {len(mismatches)} key(s): {', '.join(k for k, _ in mismatches)}",
        )
