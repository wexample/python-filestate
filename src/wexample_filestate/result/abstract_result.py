from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.item.abstract_item_target import AbstractItemTarget
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.mixin.printable_mixin import PrintableMixin
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.item.abstract_item_target import AbstractItemTarget
    from wexample_filestate.operation.abstract_operation import AbstractOperation


@base_class
class AbstractResult(PrintableMixin, BaseClass):
    operations: list[AbstractOperation] = public_field(
        factory=list,
        description="List of operations performed in this result",
    )
    rollback: bool = public_field(
        default=False,
        description="Indicates whether a rollback should be performed",
    )
    state_manager: AbstractItemTarget = public_field(
        description="Item target state manager associated with this result",
    )

    def apply_operations(self, interactive: bool = False) -> None:
        self._executed_operations = []

        # Define order of operations based on rollback mode
        operations = reversed(self.operations) if self.rollback else self.operations

        # Apply each operation with its dependencies in the correct order
        for operation in operations:
            self.apply_with_dependencies(
                interactive=interactive,
                operation=operation,
                dry_run=True,
                rollback=self.rollback,
            )

    def apply_with_dependencies(
        self,
        operation: AbstractOperation,
        dry_run: bool = False,
        rollback: bool = False,
        interactive: bool = False,
    ) -> None:
        pass

        # Retrieve dependencies based on rollback mode
        dependencies = operation.dependencies()
        dependencies = reversed(dependencies) if rollback else dependencies

        # Execute the main operation before dependencies if rollback, otherwise after dependencies
        if rollback and operation not in self._executed_operations:
            operation.undo()
            operation.applied = False
            self._executed_operations.append(operation)

        # Apply dependencies in the specified order
        for dependency_class in dependencies:
            dependency = self._find_dependency(dependency_class)
            if dependency is not None and dependency not in self._executed_operations:
                self.apply_with_dependencies(
                    operation=dependency, interactive=dependency, rollback=rollback
                )

        # Execute the main operation after dependencies if not rollback
        if not rollback and operation not in self._executed_operations:
            self.state_manager.io.title(
                f"OPERATION: {operation.get_snake_short_class_name().upper()}"
            )
            applied = self._apply_single_operation(
                operation=operation, interactive=interactive
            )

            if applied:
                operation.applied = True
                self._executed_operations.append(operation)

                self.state_manager.io.task(
                    message=f"{operation.target.get_item_title()}: {operation.target.render_display_path()}\n"
                    f"    → {operation.description()}\n"
                    f"    ⋮ Before : {operation.describe_before()}\n"
                    f"    ⋮ After  : {operation.describe_after()}",
                )
            else:
                self.state_manager.io.log(
                    message=f"{operation.target.get_item_title()}: {operation.target.render_display_path()}\n"
                    f"    → {operation.description()}\n"
                    f"    ⋮ Operation aborted"
                )

    @abstract_method
    def _apply_single_operation(
        self, operation: AbstractOperation, interactive: bool = False
    ) -> bool:
        pass
