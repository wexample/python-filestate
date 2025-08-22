from __future__ import annotations

from abc import ABC
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from wexample_config.config_option.abstract_nested_config_option import (
    AbstractNestedConfigOption,
)
from wexample_config.const.types import DictConfig
from wexample_file.const.types import PathOrString
from wexample_filestate.config_option.mixin.item_config_option_mixin import (
    ItemTreeConfigOptionMixin,
)
from wexample_filestate.enum.scopes import Scope
from wexample_filestate.item.mixins.item_mixin import ItemMixin
from wexample_filestate.operations_provider.abstract_operations_provider import (
    AbstractOperationsProvider,
)
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.mixins.with_required_io_manager import WithRequiredIoManager

if TYPE_CHECKING:
    from wexample_config.options_provider.abstract_options_provider import (
        AbstractOptionsProvider,
    )
    from wexample_filestate.const.state_items import SourceFileOrDirectory
    from wexample_filestate.const.types_state_items import (
        SourceFileOrDirectoryType,
        TargetFileOrDirectoryType,
    )
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.result.abstract_result import AbstractResult
    from wexample_filestate.result.file_state_dry_run_result import (
        FileStateDryRunResult,
    )
    from wexample_filestate.result.file_state_result import FileStateResult
    from wexample_prompt.common.io_manager import IoManager


class AbstractItemTarget(
    WithRequiredIoManager,
    ItemMixin,
    ItemTreeConfigOptionMixin,
    AbstractNestedConfigOption,
    ABC,
):
    source: SourceFileOrDirectory | None = None
    operations_providers: list[type[AbstractOperationsProvider]] | None = None
    last_result: AbstractResult | None = None

    def __init__(self, io: "IoManager", **kwargs) -> None:
        ItemMixin.__init__(self, **kwargs)
        AbstractNestedConfigOption.__init__(self, **kwargs)
        WithRequiredIoManager.__init__(self, io=io)

    @classmethod
    def create_from_path(
        cls, path: PathOrString, config: DictConfig | None = None, **kwargs
    ) -> "AbstractItemTarget":
        from wexample_helpers.helpers.directory import (
            directory_get_base_name,
            directory_get_parent_path,
        )

        config = config or {}

        manager = cls(base_path=directory_get_parent_path(path), **kwargs)

        config["name"] = (
            config["name"] if config.get("name") else directory_get_base_name(path)
        )
        manager.configure(config=config)
        return manager

    @classmethod
    def create_from_config(cls, **kwargs) -> AbstractItemTarget:
        config = kwargs.get("config")
        instance = cls(**kwargs)
        instance.configure(config)

        return instance

    def configure(self, config: DictConfig) -> None:
        self.set_value(raw_value=config)
        self.locate_source(self.get_path())

    def locate_source(self, path: Path) -> "SourceFileOrDirectoryType":
        if path.is_file():
            from wexample_filestate.item.item_source_file import ItemSourceFile

            self.source = ItemSourceFile(
                path=path,
            )
        elif path.is_dir():
            from wexample_filestate.item.item_source_directory import (
                ItemSourceDirectory,
            )

            self.source = ItemSourceDirectory(
                path=path,
            )

        return self.source

    def get_path(self) -> Path:
        # Base path is specified, for instance for the tree root.
        if self.base_path is not None:
            base_path = self.base_path
        else:
            base_path = self.get_parent_item().get_resolved()

        return Path(f"{base_path}{self.get_item_name()}")

    def get_operations(self) -> list[type["AbstractOperation"]]:
        providers = self.get_operations_providers()
        operations = []

        for provider in providers:
            operations.extend(
                cast("AbstractOperationsProvider", provider).get_operations()
            )

        return operations

    def get_options_providers(self) -> list[type["AbstractOptionsProvider"]]:
        providers = super().get_options_providers()
        if len(providers) > 0:
            return providers

        from wexample_filestate.options_provider.default_options_provider import (
            DefaultOptionsProvider,
        )

        return [
            DefaultOptionsProvider,
        ]

    def build_operations(
        self: "TargetFileOrDirectoryType",
        result: "AbstractResult",
        scopes: set[Scope] | None = None,
    ) -> None:
        self.io.indentation_up()
        self.io.log(f"Building operations for: {self.get_path()}")

        for operation_class in self.get_operations():
            if operation_class.applicable(self) and (
                scopes is None or operation_class.get_scope() in scopes
            ):
                self.io.log(
                    f"Building operation: {operation_class.get_snake_short_class_name()}"
                )
                result.operations.append(operation_class(io=self.io, target=self))

        self.io.indentation_down()

    def get_operations_providers(self) -> list[type["AbstractOperationsProvider"]]:
        if self.parent:
            return cast(
                AbstractItemTarget, self.get_parent_item()
            ).get_operations_providers()

        if self.operations_providers:
            return self.operations_providers

        from wexample_filestate.operations_provider.default_operations_provider import (
            DefaultOperationsProvider,
        )

        return [
            DefaultOperationsProvider,
        ]

    def get_item_name(self) -> str:
        from wexample_config.config_option.name_config_option import NameConfigOption

        return self.get_option(NameConfigOption).get_value().get_str()

    def get_source(self) -> "SourceFileOrDirectory":
        assert self.source is not None
        return self.source

    def dump(self) -> Any:
        output = super().dump()
        output["name"] = self.get_item_name()

        return output

    def rollback(self) -> "FileStateResult":
        from wexample_filestate.result.file_state_result import FileStateResult

        result = FileStateResult(state_manager=self, rollback=True)

        # Fetch applied operations to a new stack.
        if self.last_result:
            for operation in self.last_result.operations:
                if operation.applied:
                    result.operations.append(operation)

        result.apply_operations()
        self.last_result = result

        return result

    def dry_run(self, scopes: set[Scope] | None = None) -> "FileStateDryRunResult":
        from wexample_filestate.result.file_state_dry_run_result import (
            FileStateDryRunResult,
        )

        result = FileStateDryRunResult(state_manager=self)
        self.last_result = result
        self.build_operations(result=result, scopes=scopes)
        result.apply_operations()

        return result

    def apply(
        self,
        interactive: bool = False,
        scopes: set[Scope] | None = None,
        verbosity: VerbosityLevel | None = VerbosityLevel.DEFAULT,
    ) -> "FileStateResult":
        from wexample_filestate.result.file_state_result import FileStateResult

        result = FileStateResult(state_manager=self)
        self.last_result = result
        self.build_operations(result=result, scopes=scopes)

        if len(result.operations) > 0:
            result.apply_operations(interactive=interactive)
        else:
            from wexample_helpers.helpers.cli import cli_make_clickable_path

            self.io.info(
                message=f"No operation to execute on: {cli_make_clickable_path(self.get_path())} ",
                verbosity=verbosity,
            )

        return result
