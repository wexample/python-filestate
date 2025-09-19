from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_filestate.option.default_content_option import DefaultContentOption
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class ShouldExistOption(OptionMixin, AbstractConfigOption):
    value: Any = public_field(
        default=None,
        description="Boolean flag indicating whether the option must exist",
    )

    def __attrs_post_init__(self) -> None:
        super().__attrs_post_init__()
        # Replace None with True (preserves existing values)
        if self.value is None:
            self.value = True

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return bool

    def create_required_operation(self, target: TargetFileOrDirectoryType) -> AbstractOperation | None:
        """Create FileCreateOperation or FileRemoveOperation based on should_exist value and current state."""

        # Get the should_exist value
        should_exist_value = self.get_value()
        if should_exist_value is None:
            return None

        should_exist = should_exist_value.is_true() if hasattr(should_exist_value, 'is_true') else bool(should_exist_value)
        
        # Check current existence state
        exists = target.source is not None

        # Create operation based on mismatch
        if should_exist and not exists:
            # File should exist but doesn't - create it
            return self._create_file_create_operation(target=target)
        elif not should_exist and exists:
            # File shouldn't exist but does - remove it
            return self._create_file_remove_operation(target=target)

        # No operation needed if state matches expectation
        return None

    def _create_file_create_operation(self, target: TargetFileOrDirectoryType):
        from wexample_filestate.operation.file_create_operation import FileCreateOperation

        default_content_option = target.get_option(DefaultContentOption)
        default_content = None
        if default_content_option:
            default_content = default_content_option.get_value().to_str_or_none()

        return FileCreateOperation(
            option=self,
            target=target,
            default_content=default_content
        )

    def _create_file_remove_operation(self, target: TargetFileOrDirectoryType):
        from wexample_filestate.operation.file_remove_operation import FileRemoveOperation

        return FileRemoveOperation(options=self, target=target)
