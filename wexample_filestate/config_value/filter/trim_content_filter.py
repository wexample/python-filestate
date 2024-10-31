from wexample_filestate.config_value.filter.abstract_config_value_filter import AbstractConfigValueFilter


class TrimConfigValueFilter(AbstractConfigValueFilter):
    def apply_filter(self, content: str) -> str:
        return content.strip()
