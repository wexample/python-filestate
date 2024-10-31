from pathlib import Path
from typing import TYPE_CHECKING, Any, List, Optional, Type, Union, cast

from wexample_config.config_option.abstract_nested_config_option import (
    AbstractNestedConfigOption,
)
from wexample_config.const.types import DictConfig
from wexample_filestate.item.file_state_item_directory_source import (
    FileStateItemDirectorySource,
)
from wexample_filestate.item.file_state_item_file_source import FileStateItemFileSource
from wexample_filestate.operations_provider.abstract_operations_provider import (
    AbstractOperationsProvider,
)
from wexample_helpers.const.types import FileStringOrPath

if TYPE_CHECKING:
    from wexample_config.options_provider.abstract_options_provider import (
        AbstractOptionsProvider,
    )
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.result.abstract_result import AbstractResult

# Might become the real type, and rename current SourceFileOrDirectoryAnnotation
SourceFileOrDirectory = Union[FileStateItemDirectorySource, FileStateItemFileSource]


class StateItemTargetMixin(AbstractNestedConfigOption):
    base_path: FileStringOrPath
    path: Optional[Path] = None
    source: Optional[SourceFileOrDirectory] = None
    operations_providers: Optional[List[Type[AbstractOperationsProvider]]] = None
    parent_item: Any = None

    def __init__(self, config: DictConfig, **data):
        AbstractNestedConfigOption.__init__(self, value=config, **data)

        self.path = Path(f"{self.base_path}{config['name']}")

        if self.path.is_file():
            from wexample_filestate.item.file_state_item_file_source import FileStateItemFileSource
            self.source = FileStateItemFileSource(
                path=self.path)
        elif self.path.is_dir():
            from wexample_filestate.item.file_state_item_directory_source import FileStateItemDirectorySource
            self.source = FileStateItemDirectorySource(
                path=self.path)

    def get_operations(self) -> List[Type["AbstractOperation"]]:
        providers = self.get_operations_providers()
        operations = []

        for provider in providers:
            operations.extend(
                cast("AbstractOperationsProvider", provider).get_operations()
            )

        return operations

    def get_options_providers(self) -> List[Type["AbstractOptionsProvider"]]:
        providers = super().get_options_providers()
        if len(providers) > 0:
            return providers

        from wexample_filestate.options_provider.default_options_provider import (
            DefaultOptionsProvider,
        )

        return [
            DefaultOptionsProvider,
        ]

    def build_operations(self, result: "AbstractResult"):
        from wexample_filestate.const.types_state_items import TargetFileOrDirectory

        for operation_class in self.get_operations():
            self_casted = cast(TargetFileOrDirectory, self)
            if operation_class.applicable(self_casted):
                result.operations.append(operation_class(target=self_casted))

    def get_operations_providers(self) -> List[Type["AbstractOperationsProvider"]]:
        if self.parent_item:
            return cast(
                StateItemTargetMixin, self.parent_item
            ).get_operations_providers()

        if self.operations_providers:
            return self.operations_providers

        from wexample_filestate.operations_provider.default_operations_provider import (
            DefaultOperationsProvider,
        )

        return [
            DefaultOperationsProvider,
        ]

    def get_item_name(self) -> Optional[str]:
        from wexample_config.config_option.name_config_option import NameConfigOption

        option = self.get_option(NameConfigOption)

        return option.get_value().get_str() if option else None

    def get_source(self) -> SourceFileOrDirectory:
        assert self.source is not None
        return self.source
