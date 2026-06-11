from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from attrs import Factory

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.exception.undefined_exception import UndefinedException

if TYPE_CHECKING:
    from wexample_filestate.item.abstract_item_target import AbstractItemTarget


def _build_child_not_found_message(self: ChildNotFoundException) -> str:
    context = (
        f" in {self.root_item.get_item_title()} '{self.root_item.get_item_name()}'"
        if self.root_item is not None
        else ""
    )
    return f"Child '{self.child}' not found{context}."


@base_class
class ChildNotFoundException(UndefinedException):
    error_code: ClassVar[str] = "FILE_STATE_CHILD_NOT_FOUND"

    child: str | None = public_field(default=None, description="Name of the missing child")
    root_item: AbstractItemTarget | None = public_field(
        default=None, description="Parent item the child was looked up in"
    )
    message: str = public_field(
        default=Factory(_build_child_not_found_message, takes_self=True),
        description="Human-readable error message",
    )
