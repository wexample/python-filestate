from __future__ import annotations

from typing import cast, Optional, TYPE_CHECKING, List, Type, Dict, Any

from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.const.types_state_items import TargetFileOrDirectory
from wexample_filestate.item.mixins.state_item_source_mixin import StateItemSourceMixin
from wexample_filestate.result.abstract_result import AbstractResult
from wexample_helpers.const.types import FileStringOrPath
from wexample_helpers.helpers.file_helper import file_resolve_path

if TYPE_CHECKING:
    from wexample_filestate.file_state_manager import FileStateManager
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.options_provider.abstract_options_provider import AbstractOptionsProvider
    from wexample_filestate.options.abstract_option import AbstractOption


class StateItemTargetMixin:
    parent: Optional[TargetFileOrDirectory] = None
    _source: Optional[StateItemSourceMixin] = None
    _options: Dict[str, AbstractOption] = {}

    @property
    def source(self):
        return self._source

    def __init__(self,
                 state_manager: 'FileStateManager',
                 path: FileStringOrPath,
                 parent: Optional[TargetFileOrDirectory] = None,
                 config: Optional[StateItemConfig] = None):
        resolved_path = file_resolve_path(path)
        if resolved_path.is_file():
            from wexample_filestate.item.file_state_item_file_source import FileStateItemFileSource
            self._source = FileStateItemFileSource(
                state_manager=state_manager,
                path=path)
        elif resolved_path.is_dir():
            from wexample_filestate.item.file_state_item_directory_source import FileStateItemDirectorySource
            self._source = FileStateItemDirectorySource(
                state_manager=state_manager,
                path=path)

        if config:
            self.configure(config)

    def operation_list_all(self) -> List[Type["AbstractOperation"]]:
        from wexample_filestate.operation.item_change_mode_operation import ItemChangeModeOperation
        from wexample_filestate.operation.file_create_operation import FileCreateOperation
        from wexample_filestate.operation.file_remove_operation import FileRemoveOperation

        return [
            FileCreateOperation,
            FileRemoveOperation,
            ItemChangeModeOperation,
        ]

    def get_options_providers(self) -> List["AbstractOptionsProvider"]:
        from wexample_filestate.options_provider.default_options_provider import DefaultOptionsProvider

        return [
            DefaultOptionsProvider()
        ]

    def get_option(self, option_type: Type["AbstractOption"]) -> Optional["AbstractOption"]:
        option_name = option_type.get_name()

        if self._options[option_name]:
            return self._options[option_name]

        return None

    def get_options(self) -> List[Type["AbstractOption"]]:
        providers = self.get_options_providers()
        options = []

        for provider in providers:
            options.extend(cast("AbstractOptionsProvider", provider).get_options())

        return options

    def configure(self, config: Optional[StateItemConfig] = None) -> None:
        if not config:
            return

        options = self.get_options()
        valid_option_names = {option_class.get_name() for option_class in options}

        unknown_keys = set(config.keys()) - valid_option_names
        if unknown_keys:
            from wexample_filestate.exceptions.invalid_option_exception import InvalidOptionException
            raise InvalidOptionException(f'Unknown configuration options: {unknown_keys}')

        for option_class in options:
            option_name = option_class.get_name()
            if option_name in config:
                self._options[option_name] = option_class(
                    target=self,
                    value=config[option_name]
                )

    def get_option_value(self, option_type: Type["AbstractOption"]) -> Any:
        option = self.get_option(option_type)
        if option:
            return option.value

        return False

    def build_operations(self, result: AbstractResult):
        from wexample_filestate.const.types_state_items import TargetFileOrDirectory

        for operation_class in self.operation_list_all():
            if operation_class.applicable(cast(TargetFileOrDirectory, self)):
                result.operations.append(operation_class(target=self))
