from __future__ import annotations

from typing import TYPE_CHECKING, cast

from wexample_filestate.item.abstract_item_target import AbstractItemTarget
from wexample_filestate.item.mixins.item_directory_mixin import ItemDirectoryMixin
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from collections.abc import Callable

    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.enum.scopes import Scope
    from wexample_filestate.result.abstract_result import AbstractResult
    from wexample_helpers.const.types import (
        FileStringOrPath,
        PathOrString,
        StringKeysDict,
    )


@base_class
class ItemTargetDirectory(ItemDirectoryMixin, AbstractItemTarget):
    shortcuts: StringKeysDict = public_field(
        factory=dict,
        description="The list of referenced shortcuts pointing to items anywhere in the tree",
    )

    @classmethod
    def create_from_path(cls, path: PathOrString, **kwargs) -> ItemTargetDirectory:
        from pathlib import Path

        # If path is a file, ignore file name a keep parent directory.
        path = Path(path)
        if path.is_file():
            path = path.parent

        return super().create_from_path(path=path, **kwargs)

    def build_item_tree(self) -> None:
        from wexample_filestate.config_option.mixin.item_config_option_mixin import (
            ItemTreeConfigOptionMixin,
        )

        super().build_item_tree()

        for option in self.options.values():
            if isinstance(option, ItemTreeConfigOptionMixin):
                option.build_item_tree()

    def build_operations(
            self,
            result: AbstractResult,
            scopes: set[Scope] | None = None,
            filter_path: str | None = None,
            filter_operation: str | None = None,
            max: int = None,
    ) -> bool:
        from wexample_filestate.const.state_items import TargetFileOrDirectory

        has_task = super().build_operations(result, scopes=scopes, filter_path=filter_path,
                                            filter_operation=filter_operation,
                                            max=max)
        count = 1 if has_task is True else 0

        for item in self.get_children_list():
            has_task_child = cast(TargetFileOrDirectory, item).build_operations(
                result=result, scopes=scopes,
                filter_path=filter_path, filter_operation=filter_operation,
                max=((max - count) if (max is not None) else None)
            )

            if has_task_child:
                count += 1
                has_task = True

            if max is not None and count == max:
                return has_task

        return has_task

    def configure_from_file(self, path: FileStringOrPath) -> None:
        from wexample_helpers_yaml.helpers.yaml_helpers import yaml_read

        if yaml_read is not None:
            self.set_value(raw_value=yaml_read(str(path)))

    def find_by_name(self, item_name: str) -> TargetFileOrDirectoryType | None:
        for child in self.get_children_list():
            if child.get_item_name() == item_name:
                return child

        return None

    def find_by_name_or_fail(self, item_name: str) -> TargetFileOrDirectoryType:
        from wexample_filestate.exception.child_not_found_exception import (
            ChildNotFoundException,
        )

        child = self.find_by_name(item_name)
        if child is None:
            raise ChildNotFoundException(child=item_name, root_item=self)

        return child

    def find_by_name_recursive(
            self, item_name: str
    ) -> TargetFileOrDirectoryType | None:
        found = self.find_by_name(item_name)
        if found:
            return found

        for child in self.get_children_list():
            if child.is_directory():
                result = cast(ItemTargetDirectory, child).find_by_name_recursive(
                    item_name
                )
                if result:
                    return result

        return None

    def find_by_path(self, path: FileStringOrPath) -> TargetFileOrDirectoryType | None:
        from pathlib import Path

        target = Path(path)

        for child in self.get_children_list():
            if child.get_path() == target:
                return child

        return None

    def find_by_path_recursive(
            self, path: FileStringOrPath
    ) -> TargetFileOrDirectoryType | None:
        from pathlib import Path

        path = Path(path)
        found = self.find_by_path(path)
        if found:
            return found

        for child in self.get_children_list():
            if child.is_directory():
                result = cast(ItemTargetDirectory, child).find_by_path_recursive(path)
                if result:
                    return result

        return None

    def for_each_child_file_recursive(self, callback: Callable) -> None:
        from wexample_filestate.item.item_target_file import ItemTargetFile

        self.for_each_child_of_type_recursive(
            class_type=ItemTargetFile,
            callback=callback,
        )

    def for_each_child_of_type(
            self,
            class_type: type[AbstractItemTarget],
            callback: Callable[[AbstractItemTarget], None],
    ) -> None:
        for child in self.get_children_list():
            if isinstance(child, class_type):
                callback(child)

    def for_each_child_of_type_recursive(
            self, class_type: type[AbstractItemTarget], callback: Callable
    ) -> None:
        def _only_type(item: AbstractItemTarget) -> None:
            if isinstance(item, class_type):
                callback(item)

        self.for_each_child_recursive(_only_type)

    def for_each_child_recursive(self, callback: Callable) -> None:
        for child in self.get_children_list():
            if isinstance(child, ItemTargetDirectory):
                child.for_each_child_recursive(callback)

            callback(child)

    def get_children_list(self) -> list[TargetFileOrDirectoryType]:
        from wexample_filestate.option.children_option import (
            ChildrenOption,
        )

        option = cast(ChildrenOption, self.get_option(ChildrenOption))
        if option is not None:
            return option.get_children()

        return []

    def get_shortcut(self, name: str) -> AbstractItemTarget | None:
        return self.shortcuts[name] if name in self.shortcuts else None

    def get_shortcut_or_fail(self, name: str) -> AbstractItemTarget | None:
        from wexample_filestate.exception.undefined_shortcut_exception import (
            UndefinedShortcutException,
        )

        shortcut = self.get_shortcut(name=name)

        if shortcut is None:
            raise UndefinedShortcutException(shortcut=name, root_item=self)

    def set_shortcut(self, name: str, children: AbstractItemTarget) -> None:
        from wexample_filestate.exception.existing_shortcut_exception import (
            ExistingShortcutException,
        )

        if name in self.shortcuts:
            raise ExistingShortcutException(
                shortcut=name,
                new_item=children,
                existing_item=self.shortcuts[name],
                root_item=self,
            )

        self.shortcuts[name] = children
