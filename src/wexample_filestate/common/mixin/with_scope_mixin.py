from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method

if TYPE_CHECKING:
    from wexample_filestate.enum.scopes import Scope


class WithScopeMixin:
    @classmethod
    @abstract_method
    def get_scopes(cls) -> list[Scope]:
        pass

    @classmethod
    def matches_scope_filter(cls, scopes: Iterable[Scope]) -> bool:
        """
        Return True when the provided scope filter should allow instances of this class.

        Classes must declare their scopes explicitly.
        """
        declared_scopes = cls.get_scopes()

        declared_set = set(declared_scopes)
        filter_set = set(scopes)

        return len(declared_set.intersection(filter_set)) > 0
