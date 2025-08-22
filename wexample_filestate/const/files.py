from typing_extensions import TypedDict


class FileSystemPermissionConfig(TypedDict):
    mode: int
    recursive: bool


FileSystemPermission = FileSystemPermissionConfig | str | int
