from pydantic import Field

from wexample_filestate.const.state_items import TargetFileOrDirectory
from wexample_helpers.classes.extended_base_model import ExtendedBaseModel


class SearchResult(ExtendedBaseModel):
    item: TargetFileOrDirectory = Field()
    searched: str = Field()
    line: int = Field()
    column: int = Field()
