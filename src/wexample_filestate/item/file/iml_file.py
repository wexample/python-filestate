from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_filestate.item.file.xml_file import XmlFile

if TYPE_CHECKING:
    pass


class ImlFile(XmlFile):
    """
    Simple .iml reader/writer using python-dotenv.
    """

    EXTENSION_ENV: ClassVar[str] = "iml"
    EXTENSION_DOT_ENV: ClassVar[str] = f".{EXTENSION_ENV}"
