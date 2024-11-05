from typing import cast

from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class ItemTreeConfigOptionMixin:
    """
    Give properties to every option that can be a part of the file system configuration tree,
    like any file or directory descriptor, and also children option a children factories.
    """

    def get_parent_item(self) -> "TargetFileOrDirectoryType":
        from wexample_filestate.const.state_items import TargetFileOrDirectory

        # In all case, when asking for parent item,
        # every config option should be an item tree item.
        assert isinstance(self.parent, ItemTreeConfigOptionMixin)

        if isinstance(self.parent, TargetFileOrDirectory):
            return cast(TargetFileOrDirectoryType, self.parent)

        # give a try to parent.
        return cast(TargetFileOrDirectoryType, self.parent).get_parent_item()
