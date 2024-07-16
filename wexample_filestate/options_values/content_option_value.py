from typing import List, Optional

from wexample_filestate.options_values.content_filter.abstract_content_filter import AbstractContentFilter
from wexample_filestate.options_values.string_option_value import StringOptionValue


class ContentOptionValue(StringOptionValue):
    filters: List[AbstractContentFilter]

    def __init__(self, filters: Optional[List[AbstractContentFilter]] = None, **kwargs) -> None:
        super().__init__(filters=filters or [], **kwargs)
