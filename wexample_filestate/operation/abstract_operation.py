from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Union

from pydantic import BaseModel

if TYPE_CHECKING:
    from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
    from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget


class AbstractOperation(BaseModel):
    @classmethod
    def get_name(cls):
        return cls.__name__.lower()

    @staticmethod
    @abstractmethod
    def applicable(target: Union["FileStateItemDirectoryTarget", "FileStateItemFileTarget"]) -> bool:
        pass

    @abstractmethod
    def apply(self) -> None:
        pass
