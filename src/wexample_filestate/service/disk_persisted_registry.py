from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.service.registry import Registry

if TYPE_CHECKING:
    from wexample_filestate.item.file.structured_content_file import (
        StructuredContentFile,
    )

T = TypeVar("T")


@base_class
class DiskPersistedRegistry(Registry[T]):
    """Registry whose state is persisted to disk via a StructuredContentFile.

    The file (YamlFile, JsonFile, ...) is provided at construction. Items
    should implement serialize() / hydrate(data) when participating in the
    persisted state — otherwise they are stored as-is in the file payload.
    """

    _file: StructuredContentFile | None = private_field(
        default=None, description="StructuredContentFile backing the registry"
    )

    def __init__(
        self, container: Any = None, file: StructuredContentFile | None = None
    ) -> None:
        super().__init__(container=container)
        self._file = file

    def is_persisted(self) -> bool:
        """True if the backing file exists on disk and has content."""
        if self._file is None:
            return False
        try:
            return not self._file.get_local_file().is_empty()
        except FileNotFoundError:
            return False

    def load(self, item_class: type[T] | None = None) -> None:
        """Hydrate the registry from the backing file.

        If item_class implements hydrate(data) (Registrable), instances are
        created from each payload entry. Otherwise raw entries are stored.
        Missing file is treated as an empty payload (no-op).
        """
        if self._file is None:
            raise RuntimeError("No StructuredContentFile configured for persistence")
        if not self.is_persisted():
            return
        data = self._file.read_parsed() or {}
        _use_hydrate = item_class is not None and hasattr(item_class, "hydrate")
        for key, entry in data.items():
            self._items[key] = item_class.hydrate(entry) if _use_hydrate else entry

    def save(self) -> None:
        """Serialize current items to the backing file.

        Items implementing serialize() are converted; others are kept raw.
        """
        if self._file is None:
            raise RuntimeError("No StructuredContentFile configured for persistence")
        payload = {
            key: (item.serialize() if hasattr(item, "serialize") else item)
            for key, item in self._items.items()
        }
        self._file.write_parsed(payload)
