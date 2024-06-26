from wexample_filestate.options.abstract_option import AbstractOption


class RemoveBackupMaxFileSizeOption(AbstractOption):
    value: int = 1000

    @staticmethod
    def get_name() -> str:
        return "remove_backup_max_file_size"
