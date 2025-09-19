from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_option.abstract_nested_config_option import AbstractNestedConfigOption
from wexample_file.enum.local_path_type import LocalPathType
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class YamlOption(OptionMixin, AbstractNestedConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.config_value.yaml_config_value import YamlConfigValue
        return Union[dict, YamlConfigValue]

    def applicable_on_directory(self) -> bool:
        return False

    def applicable_on_missing(self) -> bool:
        return False

    def get_supported_item_types(self) -> list[LocalPathType]:
        return [
            LocalPathType.FILE,
        ]

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.config_option.sort_recursive_config_option import SortRecursiveConfigOption

        return [
            SortRecursiveConfigOption,
        ]

    def create_required_operation(self, target: TargetFileOrDirectoryType) -> AbstractOperation | None:
        """Create YamlSortRecursiveOperation if sort_recursive is enabled and file needs sorting."""
        from wexample_filestate.config_option.sort_recursive_config_option import SortRecursiveConfigOption
        from wexample_filestate.operation.file_write_operation import FileWriteOperation
        import yaml
        from wexample_helpers_yaml.helpers.yaml_helpers import yaml_read

        # Check if sort_recursive is enabled
        sort_recursive_option = self.get_option_value(SortRecursiveConfigOption, default=False)
        if not sort_recursive_option.is_true():
            return None

        # Check if file needs sorting
        if self._is_yaml_sorted(target):
            return None

        # Read and sort the YAML content
        data = yaml_read(target.get_path())

        def sort_rec(obj):
            if isinstance(obj, dict):
                return {k: sort_rec(obj[k]) for k in sorted(obj.keys())}
            if isinstance(obj, list):
                return [sort_rec(v) for v in obj]
            return obj

        sorted_data = sort_rec(data)
        sorted_content = yaml.safe_dump(sorted_data, sort_keys=False)

        return FileWriteOperation(
            option=self, 
            target=target, 
            content=sorted_content,
            description="Sort YAML file content recursively"
        )

    def _is_yaml_sorted(self, target: TargetFileOrDirectoryType) -> bool:
        """Check if YAML file is already recursively sorted."""
        import yaml
        from wexample_helpers_yaml.helpers.yaml_helpers import yaml_read

        data = yaml_read(target.get_path())

        def sort_rec(obj):
            if isinstance(obj, dict):
                return {k: sort_rec(obj[k]) for k in sorted(obj.keys())}
            if isinstance(obj, list):
                return [sort_rec(v) for v in obj]
            return obj

        sorted_data = sort_rec(data)
        current_dump = yaml.safe_dump(data, sort_keys=False)
        sorted_dump = yaml.safe_dump(sorted_data, sort_keys=False)
        return current_dump == sorted_dump

