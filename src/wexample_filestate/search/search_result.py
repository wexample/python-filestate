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
        if search in item.read():
            return cls(
                item=item,
                # TODO line and col
            )
        return None
