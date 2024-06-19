from __future__ import annotations

from wexample_filestate.item.file_state_item_directory import FileStateItemDirectory
from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget


class FileStateItemDirectoryTarget(FileStateItemDirectory):
    def configure(self, config: dict):
        base_path = self.get_resolved()

        if 'files' in config:
            for file in config['files']:
                FileStateItemFileTarget(path=base_path + file['name'])

        if 'directories' in config:
            for directory in config['directories']:
                FileStateItemDirectoryTarget(path=base_path + directory['path'])
