from wexample_filestate.item.abstract_file_state_item import AbstractFileStateItem
from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget


class FileStateItemFileSource(AbstractFileStateItem):
    def create_target(self) -> FileStateItemFileTarget:
        return FileStateItemFileTarget(path=self.path)
