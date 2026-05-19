from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.result.abstract_result import AbstractResult

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation


class FileStateDryRunResult(AbstractResult):
    def _apply_single_operation(
        self, operation: AbstractOperation, interactive: bool = False
    ) -> bool:
        return True

    def apply_operations(self, interactive: bool = False) -> None:
        # Dry-run does no I/O — parallelization adds thread-pool overhead with
        # zero benefit. Force the sequential path.
        self._executed_operations = []
        self._apply_operations_sequential(interactive=interactive)
