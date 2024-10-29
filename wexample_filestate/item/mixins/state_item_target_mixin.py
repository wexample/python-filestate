from typing import List, Type, Optional, TYPE_CHECKING, cast, Any
from pathlib import Path

from pydantic import BaseModel
from wexample_config.classes.config_manager import ConfigManager
from wexample_config.const.types import DictConfig
from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider
from wexample_filestate.const.types_state_items import TargetFileOrDirectory
from wexample_filestate.operations_provider.abstract_operations_provider import AbstractOperationsProvider
from wexample_filestate.item.mixins.state_item_source_mixin import StateItemSourceMixin
from wexample_helpers.const.types import FileStringOrPath

if TYPE_CHECKING:
    from wexample_filestate.result.abstract_result import AbstractResult
    from wexample_filestate.operation.abstract_operation import AbstractOperation


class StateItemTargetMixin(ConfigManager, BaseModel):
    base_path: FileStringOrPath
    path: Optional[Path] = None
    source: Optional[StateItemSourceMixin] = None
    options_providers: Optional[List[Type["AbstractOptionsProvider"]]] = None
    operations_providers: Optional[List[Type["AbstractOperationsProvider"]]] = None
    parent: Optional[TargetFileOrDirectory] = None

    def __init__(self, config: DictConfig, **data):
        BaseModel.__init__(self, config=config, **data)
        ConfigManager.__init__(self, config=config, **data)

        self.path = Path(f"{self.base_path}{config['name']}")

        self.configure(config=config)

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
            operations.extend(cast("AbstractOperationsProvider", provider).get_operations())

        return operations

    def get_options_providers(self) -> List[Type["AbstractOptionsProvider"]]:
        if self.parent:
            return self.parent.get_options_providers()

        if self.options_providers:
            return self.options_providers

        from wexample_filestate.options_provider.default_options_provider import DefaultOptionsProvider

        return [
            DefaultOptionsProvider,
        ]

    def get_operations_providers(self) -> List[Type["AbstractOperationsProvider"]]:
        if self.parent:
            return self.parent.get_operations_providers()

        if self.operations_providers:
            return self.operations_providers

        from wexample_filestate.operations_provider.default_operations_provider import DefaultOperationsProvider

        return [
            DefaultOperationsProvider,
        ]

    def build_operations(self, result: "AbstractResult"):
        from wexample_filestate.const.types_state_items import TargetFileOrDirectory

        for operation_class in self.get_operations():
            if operation_class.applicable(cast(TargetFileOrDirectory, self)):
                result.operations.append(operation_class(target=self))

    def get_name(self) -> Optional[str]:
        from wexample_config.option.name_config_option import NameConfigOption
        option = self.get_option(NameConfigOption)

        return option.value.get_str() if option else None
