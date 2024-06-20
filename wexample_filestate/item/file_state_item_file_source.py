from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
from wexample_filestate.item.file_state_item_file import FileStateItemFile
from wexample_filestate.item.mixins.state_item_source_mixin import StateItemSourceMixin


class FileStateItemFileSource(FileStateItemFile, StateItemSourceMixin):

    def create_target(self) -> FileStateItemDirectoryTarget:
        return FileStateItemDirectoryTarget(path=self.path)

