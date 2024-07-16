from wexample_filestate.options_values.content_filter.abstract_content_filter import AbstractContentFilter


class TrimContentFilter(AbstractContentFilter):
    def apply_filter(self, content: str) -> str:
        return content.strip()
