from wexample_filestate.options.abstract_option import AbstractOption


class NameOption(AbstractOption):
    @staticmethod
    def get_name() -> str:
        return "name"
