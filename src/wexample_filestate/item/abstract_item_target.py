from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from wexample_config.config_option.abstract_nested_config_option import (
    AbstractNestedConfigOption,
)
from wexample_filestate.config_option.mixin.item_config_option_mixin import (
    ItemTreeConfigOptionMixin,
)
from wexample_filestate.item.mixins.item_mixin import ItemMixin
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_prompt.mixins.with_io_methods import WithIoMethods

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_config.const.types import DictConfig
    from wexample_config.options_provider.abstract_options_provider import (
        AbstractOptionsProvider,
    )
    from wexample_filestate.const.state_items import SourceFileOrDirectory
    from wexample_filestate.const.types_state_items import (
        SourceFileOrDirectoryType,
        TargetFileOrDirectoryType,
    )
    from wexample_filestate.enum.scopes import Scope
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.operations_provider.abstract_operations_provider import (
        AbstractOperationsProvider,
    )
    from wexample_filestate.result.abstract_result import AbstractResult
    from wexample_filestate.result.file_state_dry_run_result import (
        FileStateDryRunResult,
    )
    from wexample_filestate.result.file_state_result import FileStateResult
    from wexample_helpers.const.types import PathOrString


@base_class
class AbstractItemTarget(
    WithIoMethods,
    ItemMixin,
    ItemTreeConfigOptionMixin,
    AbstractNestedConfigOption,
):
    last_result: AbstractResult | None = public_field(
        default=None, description="The last applied result of state operation"
    )
    operations_providers: list[type[AbstractOperationsProvider]] | None = public_field(
        default=None, description="List of operations providers"
    )
    source: SourceFileOrDirectory | None = public_field(
        default=None, description="The original existing file or directory"
    )

    @classmethod
    def create_from_config(cls, **kwargs) -> AbstractItemTarget:
        config = kwargs.get("config")
        kwargs.pop("config", None)
        instance = cls(**kwargs)
        instance.configure(config)

        return instance

    @classmethod
    def create_from_path(
            cls, path: PathOrString, config: DictConfig | None = None, **kwargs
    ) -> AbstractItemTarget:
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

    def apply(
            self,
            interactive: bool = False,
            scopes: set[Scope] | None = None,
            filter_path: str | None = None,
            filter_operation: str | None = None,
            max: int = None,
    ) -> FileStateResult:
        from wexample_filestate.result.file_state_result import FileStateResult
        from wexample_helpers.helpers.cli import cli_make_clickable_path

        result = FileStateResult(state_manager=self)
        self.last_result = result
        self.build_operations(result=result, scopes=scopes, filter_path=filter_path, filter_operation=filter_operation,
                              max=max)

        if len(result.operations) > 0:
            # Execute only the first operation (single operation per run)
            if len(result.operations) > 1:
                self.io.info(f"Found {len(result.operations)} operations, executing only the first one")
                result.operations = result.operations[:1]
            
            result.apply_operations(interactive=interactive)
        else:
            self.io.info(
                message=f"No operation to execute on: {cli_make_clickable_path(self.get_path())} ",
            )

        return result

    def _find_first_required_operation(
        self: TargetFileOrDirectoryType,
        scopes: set[Scope] | None = None,
        filter_operation: str | None = None,
    ) -> AbstractOperation | None:
        """Find the first option that requires an operation and return it.
        
        Returns None if no operation is required.
        """
        for option in self.options.values():
            operation = self._try_create_operation_from_option(option, scopes, filter_operation)
            if operation is not None:
                return operation
        return None

    def _try_create_operation_from_option(
        self: TargetFileOrDirectoryType,
        option,
        scopes: set[Scope] | None = None,
        filter_operation: str | None = None,
    ) -> AbstractOperation | None:
        """Try to create an operation from an option.
        
        Returns None if no operation is needed or if the option doesn't support the new interface.
        """
        # Skip if option doesn't have the new method (backward compatibility)
        if not self._option_supports_new_interface(option):
            return None

        # Create the required operation (returns None if satisfied/not applicable)
        operation = option.create_required_operation(self)
        if operation is None:
            return None

        # Apply filters
        if not self._operation_passes_filters(operation, scopes, filter_operation):
            return None

        return operation

    def _option_supports_new_interface(self, option) -> bool:
        """Check if option supports the new create_required_operation interface."""
        return hasattr(option, 'create_required_operation')

    def _operation_passes_filters(
        self,
        operation: AbstractOperation,
        scopes: set[Scope] | None = None,
        filter_operation: str | None = None,
    ) -> bool:
        """Check if operation passes the provided filters."""
        if filter_operation is not None and not operation.__class__.matches_filter(filter_operation):
            return False
            
        if scopes is not None and operation.get_scope() not in scopes:
            return False
            
        return True

    def _path_matches(self, filter_path: str) -> bool:
        import fnmatch
        return fnmatch.fnmatch(str(self.get_path()), filter_path)

    def build_operations(
            self: TargetFileOrDirectoryType,
            result: AbstractResult,
            scopes: set[Scope] | None = None,
            filter_path: str | None = None,
            filter_operation: str | None = None,
            max: int = None,
    ) -> bool:
        from wexample_filestate.option.active_option import (
            ActiveOption,
        )
        from wexample_prompt.common.spinner_pool import SpinnerPool
        from wexample_prompt.enums.verbosity_level import VerbosityLevel

        if filter_path is not None and not self._path_matches(filter_path=filter_path):
            return None

        self.io.indentation_up()

        active_option = self.get_option(ActiveOption)

        # Allow to set active to false
        if not active_option or ActiveOption.is_active(
                active_option.get_value().raw
        ):
            loading_log = self.io.log(
                message=f"{SpinnerPool.next()} {self.get_display_path()}",
            )

            has_task: bool = False
            
            # NEW APPROACH: Iterate through options instead of operations
            operation = self._find_first_required_operation(scopes, filter_operation)
            if operation is not None:
                has_task = True
                self.io.task(
                    f'Required operation from option: "{operation.__class__.get_snake_short_class_name()}"'
                )
                result.operations.append(operation)

            if (
                    not has_task
                    and self.io.default_context_verbosity != VerbosityLevel.MAXIMUM
            ):
                self.io.erase_response(loading_log)

        self.io.indentation_down()
        return has_task

    def configure(self, config: DictConfig) -> None:
        self.set_value(raw_value=config)
        self.locate_source(self.get_path())

    def dry_run(
            self,
            scopes: set[Scope] | None = None,
            filter_path: str | None = None,
            filter_operation: str | None = None,
            max: int = None,
    ) -> FileStateDryRunResult:
        from wexample_filestate.result.file_state_dry_run_result import (
            FileStateDryRunResult,
        )

        result = FileStateDryRunResult(state_manager=self)
        self.last_result = result
        self.build_operations(result=result, scopes=scopes, filter_path=filter_path, filter_operation=filter_operation, max=max)
        result.apply_operations()

        return result

    def dump(self) -> Any:
        output = super().dump()
        output["name"] = self.get_item_name()

        return output

    def find_closest(
            self, class_type: type[AbstractItemTarget]
    ) -> AbstractItemTarget | None:
        """Return the nearest parent item that is an instance of class_type.

        Traverses parents via self.get_parent_item_or_none() until a match is found
        or the root is reached.
        """
        current = self.get_parent_item_or_none()
        while current is not None:
            if isinstance(current, class_type):
                return current  # type: ignore[return-value]
            current = current.get_parent_item_or_none()
        return None

    def get_display_path(self) -> Path:
        return self.get_relative_path() or self.get_path()

    def get_env_parameter(self, key: str, default: str | None = None) -> str | None:
        """If no environment parameter defined by current item, ask its parent.
        The default behavior is to return default value but should be replaced by,
        for instance, .env loading in specific contexts"""
        parent_item = self.get_parent_item_or_none()
        if parent_item:
            return parent_item.get_env_parameter(
                key=key,
                default=default,
            )
        return default

    def get_item_name(self) -> str:
        from wexample_config.config_option.name_config_option import NameConfigOption

        return self.get_option(NameConfigOption).get_value().get_str()

    def get_operations(self) -> list[type[AbstractOperation]]:
        providers = self.get_operations_providers()
        operations = []

        for provider in providers:
            operations.extend(provider.get_operations())

        return operations

    def get_operations_providers(self) -> list[type[AbstractOperationsProvider]]:
        from wexample_filestate.operations_provider.default_operations_provider import (
            DefaultOperationsProvider,
        )

        if self.parent:
            return cast(
                AbstractItemTarget, self.get_parent_item()
            ).get_operations_providers()

        if self.operations_providers:
            return self.operations_providers

        return [
            DefaultOperationsProvider,
        ]

    def get_options_providers(self) -> list[type[AbstractOptionsProvider]]:
        from wexample_filestate.options_provider.default_options_provider import (
            DefaultOptionsProvider,
        )

        providers = super().get_options_providers()
        if len(providers) > 0:
            return providers

        return [
            DefaultOptionsProvider,
        ]

    def get_path(self) -> Path:
        from pathlib import Path

        # Base path is specified, for instance for the tree root.
        if self.base_path is not None:
            base_path = Path(self.base_path)
        else:
            base_path = self.get_parent_item().get_path()

        return base_path / self.get_item_name()

    def get_relative_path(self) -> Path | None:
        root = self.get_root()
        if root:
            return self.get_path().relative_to(root.get_path())
        return None

    def get_source(self) -> SourceFileOrDirectory:
        assert self.source is not None
        return self.source

    def locate_source(self, path: Path) -> SourceFileOrDirectoryType:
        from wexample_filestate.item.item_source_directory import ItemSourceDirectory
        from wexample_filestate.item.item_source_file import ItemSourceFile

        if path.is_file():
            self.source = ItemSourceFile(
                path=path,
            )
        elif path.is_dir():
            self.source = ItemSourceDirectory(
                path=path,
            )

        return self.source

    def render_display_path(self) -> str:
        from wexample_helpers.helpers.cli import cli_make_clickable_path

        return cli_make_clickable_path(
            path=self.get_path(),
            short_title=self.get_display_path(),
        )

    def rollback(self) -> FileStateResult:
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
