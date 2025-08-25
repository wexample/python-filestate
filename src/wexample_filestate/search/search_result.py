from __future__ import annotations

from pydantic import Field

from wexample_filestate.item.item_target_file import ItemTargetFile
from wexample_helpers.classes.extended_base_model import ExtendedBaseModel


class SearchResult(ExtendedBaseModel):
    item: ItemTargetFile = Field()
    searched: str = Field()
    line: int = Field()
    column: int = Field()

    @classmethod
    def create_if_match(cls, search: str, item: ItemTargetFile) -> SearchResult | None:
        """Create a SearchResult if the search string is found in the file.

        Returns the first match with 1-based line and column numbers.
        """
        if not search:
            return None

        content = item.read()
        idx = content.find(search)
        if idx == -1:
            return None

        # Compute 1-based line and column
        line = content.count("\n", 0, idx) + 1
        last_nl = content.rfind("\n", 0, idx)
        column = (idx - last_nl) if last_nl != -1 else (idx + 1)

        return cls(
            item=item,
            searched=search,
            line=line,
            column=column,
        )
