from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.item.abstract_item_target import AbstractItemTarget
from wexample_filestate.item.mixins.item_directory_mixin import ItemDirectoryMixin

if TYPE_CHECKING:
    from collections.abc import Callable

    from wexample_helpers.const.types import (
        FileStringOrPath,
        PathOrString,
    )

    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.enum.scopes import Scope
    from wexample_filestate.result.abstract_result import AbstractResult


@base_class
class ItemTargetDirectory(ItemDirectoryMixin, AbstractItemTarget):
    _tree_built: bool = private_field(
        default=False,
        description="True once build_item_tree has materialized direct children. "
        "Used to make tree construction idempotent and to trigger lazy build "
        "on first get_children_list() call.",
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

        if self._tree_built:
            return
        self._tree_built = True

        super().build_item_tree()

        for option in self.options.values():
            if isinstance(option, ItemTreeConfigOptionMixin):
                option.build_item_tree()

    def build_item_tree_recursive(self) -> None:
        """Force full recursive materialization of the item tree.

        By default, build_item_tree() only materializes direct children — deeper
        levels are built lazily on access. Call this method when you need the
        complete tree right now (e.g., for eager validation or bulk operations).
        """
        for child in self.get_children_list():
            if isinstance(child, ItemTargetDirectory):
                child.build_item_tree_recursive()

    def build_operations(
        self,
        result: AbstractResult,
        scopes: set[Scope],
        filter_paths: list[str] | None = None,
        filter_operation: str | None = None,
        max: int = None,
    ) -> bool:
        from wexample_filestate.const.state_items import TargetFileOrDirectory

        has_task = super().build_operations(
            result,
            scopes=scopes,
            filter_paths=filter_paths,
            filter_operation=filter_operation,
            max=max,
        )
        count = 1 if has_task is True else 0

        if self.is_active():
            for item in self.get_children_list():
                has_task_child = cast(TargetFileOrDirectory, item).build_operations(
                    result=result,
                    scopes=scopes,
                    filter_paths=filter_paths,
                    filter_operation=filter_operation,
                    max=((max - count) if (max is not None) else None),
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

    def find_all_by_type(
        self,
        class_type: type[AbstractItemTarget],
        recursive: bool = False,
        stop_at_match: bool = True,
    ) -> list[AbstractItemTarget]:
        """Collect descendants matching ``class_type``.

        With ``stop_at_match=True`` (default), a matched node is added to the
        result but its subtree is not walked. This avoids materializing inner
        trees of "boundary" entities (e.g., packages within a suite), which is
        what callers want 99% of the time. Pass ``stop_at_match=False`` to
        also enumerate nested matches.
        """
        results: list[AbstractItemTarget] = []

        if recursive:
            self._find_all_by_type_recursive(class_type, stop_at_match, results)
        else:
            for child in self.get_children_list():
                if isinstance(child, class_type):
                    results.append(child)

        return results

    def _find_all_by_type_recursive(
        self,
        class_type: type[AbstractItemTarget],
        stop_at_match: bool,
        results: list[AbstractItemTarget],
    ) -> None:
        for child in self.get_children_list():
            is_match = isinstance(child, class_type)
            if is_match:
                results.append(child)
                if stop_at_match:
                    continue
            if isinstance(child, ItemTargetDirectory):
                child._find_all_by_type_recursive(class_type, stop_at_match, results)

    def find_by_name(
        self, item_name: PathOrString, recursive: bool = False
    ) -> TargetFileOrDirectoryType | None:
        item_name = str(item_name)

        # Check direct children first
        for child in self.get_children_list():
            if child.get_item_name() == item_name:
                return child

        # Search in subdirectories if recursive
        if recursive:
            for child in self.get_children_list():
                if child.is_directory():
                    result = cast(ItemTargetDirectory, child).find_by_name(
                        item_name, recursive=True
                    )
                    if result:
                        return result

        return None

    def find_by_name_or_fail(
        self, item_name: str, recursive: bool = False
    ) -> TargetFileOrDirectoryType:
        from wexample_filestate.exception.child_not_found_exception import (
            ChildNotFoundException,
        )

        child = self.find_by_name(item_name, recursive=recursive)
        if child is None:
            raise ChildNotFoundException(child=item_name, root_item=self)

        return child

    def find_by_path(
        self, path: FileStringOrPath, recursive: bool = False
    ) -> TargetFileOrDirectoryType | None:
        from pathlib import Path

        target = Path(path)

        # If the path contains multiple parts (e.g., "subfolder/file.txt")
        parts = target.parts
        if len(parts) > 1:
            # Search for the first element of the path (the subfolder)
            first_part = parts[0]
            remaining_path = Path(*parts[1:])

            # Find the corresponding subfolder
            for child in self.get_children_list():
                if child.get_item_name() == first_part and child.is_directory():
                    # Continue the search in the subfolder
                    return cast(ItemTargetDirectory, child).find_by_path(
                        remaining_path, recursive=recursive
                    )
            return None

        # Simple search in direct children
        for child in self.get_children_list():
            # Compare by name if target is just a filename, otherwise compare full paths
            if child.get_item_name() == str(target) or child.get_path() == target:
                return child

        # If recursive, search in subdirectories
        if recursive:
            for child in self.get_children_list():
                if child.is_directory():
                    result = cast(ItemTargetDirectory, child).find_by_path(
                        target, recursive=True
                    )
                    if result:
                        return result

        return None

    def find_by_type(
        self, class_type: type[AbstractItemTarget], recursive: bool = False
    ) -> AbstractItemTarget | None:
        # Check direct children first
        for child in self.get_children_list():
            if isinstance(child, class_type):
                return child

        # Search in subdirectories if recursive
        if recursive:
            for child in self.get_children_list():
                if child.is_directory():
                    result = cast(ItemTargetDirectory, child).find_by_type(
                        class_type, recursive=True
                    )
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

        if not self._tree_built:
            self.build_item_tree()

        option = cast(ChildrenOption, self.get_option(ChildrenOption))
        if option is not None:
            return option.get_children()

        return []

    def prepare_value(self, raw_value: Any) -> Any:
        from wexample_filestate.option.children_option import (
            ChildrenOption,
        )

        key = ChildrenOption.get_name()
        if not key in raw_value:
            raw_value[key] = []

        return raw_value
