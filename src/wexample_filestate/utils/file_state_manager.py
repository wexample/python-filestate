from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.item.item_target_directory import ItemTargetDirectory

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


@base_class
class FileStateManager(ItemTargetDirectory):
    def configure(self, config: DictConfig) -> None:
        super().configure(config=config)
        # Tree is built lazily: get_children_list() triggers build_item_tree()
        # on the root, which materializes direct children only. Recursion happens
        # lazily as each child's get_children_list() is accessed.
