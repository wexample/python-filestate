from typing import TypedDict


class FileSystemStructurePermission(TypedDict):
    mode: int
    recursive: bool
