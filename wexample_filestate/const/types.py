from __future__ import annotations
from typing_extensions import TypedDict

from wexample_helpers.const.types import StringKeysDict

# Can't define key list as it can ben dynamic when using more options.
# We may use the future __extra_items__ flag in python 3.13.
# We can still be confident to the internal config check process.
StateItemConfig = StringKeysDict


class FileSystemPermissionConfig(TypedDict):
    mode: int
    recursive: bool


class OptionDefinition(TypedDict):
    name: str


FileSystemPermission = FileSystemPermissionConfig | str | int
