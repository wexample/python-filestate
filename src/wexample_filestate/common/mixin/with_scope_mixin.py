from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_filestate.enum.scopes import Scope

_DECLARED_SCOPE_SETS: dict[type, frozenset] = {}


class WithScopeMixin:
    @classmethod
    def get_scopes(cls) -> list[Scope]:
        # Default: no declared scopes — the class opts out of scope-based filtering.
        # Concrete options/operations should override to declare the scope(s) they
        # participate in (e.g. [Scope.CONTENT], [Scope.MODE]). Returning [] means
        # `matches_scope_filter()` always returns False, so this class is skipped
        # whenever a scope filter is active.
        return []

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
