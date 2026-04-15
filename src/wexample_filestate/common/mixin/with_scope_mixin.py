from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method

if TYPE_CHECKING:
    from wexample_filestate.enum.scopes import Scope

_DECLARED_SCOPE_SETS: dict[type, frozenset] = {}


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
        declared_set = _DECLARED_SCOPE_SETS.get(cls)
        if declared_set is None:
            declared_set = frozenset(cls.get_scopes())
            _DECLARED_SCOPE_SETS[cls] = declared_set

        return not declared_set.isdisjoint(scopes)
