from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.exception.undefined_exception import UndefinedException

if TYPE_CHECKING:
    from wexample_filestate.item.abstract_item_target import AbstractItemTarget


@base_class
class ChildNotFoundException(UndefinedException):
    error_code: ClassVar[str] = "FILE_STATE_CHILD_NOT_FOUND"

    child: str | None = public_field(default=None, description="Name of the missing child")
    root_item: AbstractItemTarget | None = public_field(
        default=None, description="Parent item the child was looked up in"
    )

    def _build_message(self) -> str:
        context = (
            f" in {self.root_item.get_item_title()} '{self.root_item.get_item_name()}'"
            if self.root_item is not None
            else ""
        )
        return f"Child '{self.child}' not found{context}."
