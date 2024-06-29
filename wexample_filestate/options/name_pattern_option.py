from wexample_filestate.options.abstract_option import AbstractOption


class NamePatternOption(AbstractOption):
    @staticmethod
    def get_name() -> str:
        return "name_pattern"
