from __future__ import annotations

from pydantic import Field

from wexample_filestate.item.item_target_file import ItemTargetFile
from wexample_helpers.classes.extended_base_model import ExtendedBaseModel


class SearchResult(ExtendedBaseModel):
    item: ItemTargetFile = Field()
    searched: str = Field()
    line: int = Field()
    column: int = Field()

    @staticmethod
    def _compute_line_col(content: str, idx: int) -> tuple[int, int]:
        """Return 1-based (line, column) for a 0-based index in content."""
        line = content.count("\n", 0, idx) + 1
        last_nl = content.rfind("\n", 0, idx)
        column = (idx - last_nl) if last_nl != -1 else (idx + 1)
        return line, column

    @classmethod
    def create_one_if_match(cls, search: str, item: ItemTargetFile) -> SearchResult | None:
        """Return the first match as a SearchResult or None.

        Line and column are 1-based.
        """
        if not search:
            return None

        content = item.read()
        idx = content.find(search)
        if idx == -1:
            return None

        line, column = cls._compute_line_col(content, idx)

        return cls(item=item, searched=search, line=line, column=column)

    @classmethod
    def create_for_all_matches(cls, search: str, item: ItemTargetFile) -> list[SearchResult]:
        """Return all non-overlapping matches as a list of SearchResult.

        Matches are discovered left-to-right using str.find, advancing by
        the length of the search string to avoid overlapping matches.
        Line and column are 1-based.
        """
        if not search:
            return []

        content = item.read()
        results: list[SearchResult] = []
        start = 0
        while True:
            idx = content.find(search, start)
            if idx == -1:
                break
            line, column = cls._compute_line_col(content, idx)
            results.append(cls(item=item, searched=search, line=line, column=column))
            start = idx + len(search)

        return results

    # Backward-compatibility alias (deprecated)
    @classmethod
    def create_if_match(cls, search: str, item: ItemTargetFile) -> SearchResult | None:
        """Deprecated: use create_one_if_match. Kept for compatibility."""
        return cls.create_one_if_match(search, item)
