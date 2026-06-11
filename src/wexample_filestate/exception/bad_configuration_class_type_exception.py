from __future__ import annotations

from typing import Any, ClassVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.exception.undefined_exception import UndefinedException


@base_class
class BadConfigurationClassTypeException(UndefinedException):
    class_definition: Any = public_field(
        default=None, description="Offending value provided for the 'class' option"
    )
    error_code: ClassVar[str] = "UNDEFINED_ERROR"

    def _build_message(self) -> str:
        from wexample_filestate.item.item_target_directory import ItemTargetDirectory
        from wexample_filestate.item.item_target_file import ItemTargetFile

        class_definition = self.class_definition

        # If not given a type at all, report the actual type/value
        if not isinstance(class_definition, type):
            provided_type = type(class_definition).__name__
            return (
                f"Invalid value for 'class' option: type '{provided_type}'. "
                f"Expected a class (subclass of '{ItemTargetDirectory.__name__}' or "
                f"'{ItemTargetFile.__name__}'), got {class_definition!r}."
            )

        return (
            f"Invalid class for 'class' option: '{class_definition.__module__}.{class_definition.__name__}'. "
            f"Expected a subclass of '{ItemTargetDirectory.__name__}' or "
            f"'{ItemTargetFile.__name__}'."
        )
