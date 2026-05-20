from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.operation.abstract_file_manipulation_operation import (
    AbstractFileManipulationOperation,
)

if TYPE_CHECKING:
    from wexample_filestate.enum.scopes import Scope


@base_class
class FileRenameOperation(AbstractFileManipulationOperation):
    new_name: str = public_field(
        description="The new name",
        default=False,
    )

    @classmethod
    def get_scopes(cls) -> [Scope]:
        from wexample_filestate.enum.scopes import Scope

        return [Scope.LOCATION]

    def apply_operation(self) -> None:
        self._backup_target_file()
        self._rename_target(new_name=self.new_name)

    def undo(self) -> None:
        # Rename back from the new name to the original name.
        self._rename_target(new_name=self._original_path.name)

    def _rename_target(self, new_name: str) -> None:
        if self.target.is_file():
            self.target.get_local_file().rename(new_name)
        else:
            self.target.get_local_directory().rename(new_name)

        # Sync the in-memory item: update base_name and drop memoized paths
        # on this item plus any already-materialized descendants.
        self.target.base_name = new_name
        self.target._invalidate_path_cache()
