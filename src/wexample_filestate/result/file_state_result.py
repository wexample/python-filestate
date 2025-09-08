from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.result.abstract_result import AbstractResult

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation


class FileStateResult(AbstractResult):
    _executed_operations: list = []

    def _apply_single_operation(
        self, operation: AbstractOperation, interactive: bool = False
    ) -> bool:
        from wexample_prompt.responses.interactive.confirm_prompt_response import (
            ConfirmPromptResponse,
        )

        if interactive:
            if self.state_manager.io.confirm(
                question=f"{operation.target.get_item_title()}: {operation.target.render_display_path()}\n"
                f"{operation.describe_before()}\n"
                f"Do you want to apply this operation: {operation.description()}",
                choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
                default="yes",
            ).is_ok():
                operation.apply()
                return True

            return False

        # Non interactive.
        operation.apply()
        return True

    def _find_dependency(self, dependency_class) -> AbstractOperation | None:
        for operation in self.operations:
            if isinstance(operation, dependency_class):
                return operation
        return None
