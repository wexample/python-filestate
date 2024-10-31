from typing import cast, Any
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Type

from wexample_config.config_option.abstract_nested_config_option import \
    AbstractNestedConfigOption
from wexample_config.const.types import DictConfig
from wexample_helpers.const.types import FileStringOrPath
from wexample_filestate.operations_provider.abstract_operations_provider import AbstractOperationsProvider
from wexample_filestate.item.mixins.state_item_source_mixin import StateItemSourceMixin

if TYPE_CHECKING:
    from wexample_filestate.result.abstract_result import AbstractResult
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_config.options_provider.abstract_options_provider import \
        AbstractOptionsProvider



class StateItemTargetMixin(AbstractNestedConfigOption):
    base_path: FileStringOrPath
    path: Optional[Path] = None
    source: Optional[StateItemSourceMixin] = None
    operations_providers: Optional[List[Type[AbstractOperationsProvider]]] = None
    parent_item: Any = None

    def __init__(self, config: DictConfig, **data):
        AbstractNestedConfigOption.__init__(self, value=config, **data)

        self.path = Path(f"{self.base_path}{config['name']}")

    def get_operations(self) -> List[Type["AbstractOperation"]]:
        providers = self.get_operations_providers()
        operations = []

        for provider in providers:
            operations.extend(cast("AbstractOperationsProvider", provider).get_operations())

        return operations

    def get_options_providers(self) -> List[Type["AbstractOptionsProvider"]]:
        providers = super().get_options_providers()
        if len(providers) > 0:
            return providers

        from wexample_filestate.options_provider.default_options_provider import \
            DefaultOptionsProvider

        return [
            DefaultOptionsProvider,
        ]

    def build_operations(self, result: "AbstractResult"):
        from wexample_filestate.const.types_state_items import TargetFileOrDirectory

        for operation_class in self.get_operations():
            if operation_class.applicable(cast(TargetFileOrDirectory, self)):
                result.operations.append(operation_class(target=self))

    def get_operations_providers(self) -> List[Type["AbstractOperationsProvider"]]:
        if self.parent_item:
            return cast(StateItemTargetMixin, self.parent_item).get_operations_providers()

        if self.operations_providers:
            return self.operations_providers

        from wexample_filestate.operations_provider.default_operations_provider import DefaultOperationsProvider

        return [
            DefaultOperationsProvider,
        ]

    def get_item_name(self) -> Optional[str]:
        from wexample_config.config_option.name_config_option import \
            NameConfigOption

        option = self.get_option(NameConfigOption)

        return option.get_value().get_str() if option else None
