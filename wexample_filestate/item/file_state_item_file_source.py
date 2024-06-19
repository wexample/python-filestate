from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
from wexample_filestate.item.file_state_item_file import FileStateItemFile


class FileStateItemFileSource(FileStateItemFile):

    def create_target(self) -> FileStateItemDirectoryTarget:
        return FileStateItemDirectoryTarget(path=self.path)

