from wexample_filestate.options.abstract_option import AbstractOption


class ChildrenOption(AbstractOption):
    @staticmethod
    def get_name() -> str:
        return "children"
