from wexample_filestate.options.abstract_option import AbstractOption


class ShouldExistOption(AbstractOption):
    @staticmethod
    def get_name() -> str:
        return "should_exist"
