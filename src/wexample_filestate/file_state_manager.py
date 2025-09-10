from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.item.item_target_directory import ItemTargetDirectory
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


@base_class
class FileStateManager(ItemTargetDirectory):
    # Lazy bootstrap: ensure imports are loaded once before creating from path
    @classmethod
    def create_from_path(cls, *args, **kwargs):  # type: ignore[override]
        return super().create_from_path(*args, **kwargs)

    def configure(self, config: DictConfig) -> None:
        super().configure(config=config)

        # As root
        self.build_item_tree()
