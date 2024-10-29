from typing import Protocol

from wexample_filestate.const.types_state_items import TargetFileOrDirectory


class HasTargetProtocol(Protocol):
    target: TargetFileOrDirectory
