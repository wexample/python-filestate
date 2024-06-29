from wexample_filestate.options.abstract_option import AbstractOption


class TypeOption(AbstractOption):
    @staticmethod
    def get_name() -> str:
        return "type"
