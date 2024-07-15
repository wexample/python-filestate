from pathlib import PosixPath, Path
from typing import cast, Optional, TYPE_CHECKING, List, Type, Dict, Any

from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.const.types_state_items import TargetFileOrDirectory
from wexample_filestate.item.mixins.state_item_source_mixin import StateItemSourceMixin
from wexample_filestate.result.abstract_result import AbstractResult
from wexample_helpers.helpers.file_helper import file_resolve_path
from wexample_helpers.const.types import FileStringOrPath
from wexample_filestate.options.abstract_option import AbstractOption

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.options_provider.abstract_options_provider import AbstractOptionsProvider

from pydantic import BaseModel


class StateItemTargetMixin(BaseModel):
    config: Optional[StateItemConfig] = None
    parent: Optional[TargetFileOrDirectory] = None
    base_path: FileStringOrPath
    _path: Path
    _source: Optional[StateItemSourceMixin] = None
    _options: Dict[str, AbstractOption]

    def __init__(self, config: Optional[StateItemConfig] = None, **data):
        super().__init__(**data)
        self._options = {}

        config = self.build_config(config)

        # Resolve callables and process children recursively
        for key, value in list(config.items()):
            from wexample_filestate.options_values.callback_option_value import CallbackOptionValue

            if isinstance(value, CallbackOptionValue):
                config[key] = value.callback(self, config)

        self._path = Path(f"{self.base_path}{config['name']}")

        if self._path.is_file():
            from wexample_filestate.item.file_state_item_file_source import FileStateItemFileSource
            self._source = FileStateItemFileSource(
                path=self._path)
        elif self._path.is_dir():
            from wexample_filestate.item.file_state_item_directory_source import FileStateItemDirectorySource
            self._source = FileStateItemDirectorySource(
                path=self._path)

        if config:
            self.configure(config)

    def build_config(self, config: Optional[StateItemConfig] = None) -> StateItemConfig:
        return config or {}

    @property
    def source(self):
        return self._source

    @property
    def path(self) -> Path:
        return self._path

    def get_operations(self) -> List[Type["AbstractOperation"]]:
        providers = self.get_options_providers()
        operations = []

        for provider in providers:
            operations.extend(cast("AbstractOptionsProvider", provider).get_operations())

        return operations

    def get_options_providers(self) -> List["AbstractOptionsProvider"]:
        from wexample_filestate.options_provider.default_options_provider import DefaultOptionsProvider
        from wexample_filestate.options_provider.git_options_provider import GitOptionsProvider

        return [
            DefaultOptionsProvider(),
            GitOptionsProvider()
        ]

    def get_option(self, option_type: Type["AbstractOption"]) -> Optional["AbstractOption"]:
        option_name = option_type.get_name()

        if option_name in self._options:
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
            from wexample_filestate.const.exceptions import InvalidOptionException
            raise InvalidOptionException(f'Unknown configuration option name: {unknown_keys}')

        # Loop over options classes to execute option_class.resolve_config(config)
        # This will modify config before using it, with extra configuration keys.
        for option_class in options:
            config = option_class.resolve_config(config)

        for option_class in options:
            option_name = option_class.get_name()
            if option_name in config:
                self._options[option_name] = option_class(
                    target=self,
                    value=config[option_name]
                )

    def get_name(self) -> Optional[str]:
        from wexample_filestate.options.name_option import NameOption
        option = self.get_option(NameOption)

        return option.value if option else None

    def get_option_value(self, option_type: Type["AbstractOption"], default: Any = None) -> Any:
        option = self.get_option(option_type)
        if option:
            return option.value

        return default

    def build_operations(self, result: AbstractResult):
        from wexample_filestate.const.types_state_items import TargetFileOrDirectory

        for operation_class in self.get_operations():
            if operation_class.applicable(cast(TargetFileOrDirectory, self)):
                result.operations.append(operation_class(target=self))

    def config_parse_value(self, value: Any) -> str:
        path = cast(PosixPath, self.path)

        if isinstance(value, str):
            return value
        elif isinstance(value, dict) and "pattern" in value:
            return value["pattern"].format(**{
                'name': path.name,
                'path': str(path)
            })

        return value
