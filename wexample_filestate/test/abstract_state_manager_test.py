import os
from abc import ABC
from typing import TYPE_CHECKING, Optional, List, Type

if TYPE_CHECKING:
    from wexample_filestate.file_state_manager import FileStateManager
    from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider
    from wexample_filestate.operations_provider.abstract_operations_provider import AbstractOperationsProvider


class AbstractStateManagerTest(ABC):
    state_manager: "FileStateManager"

    def _get_package_root_path(self) -> str:
        return os.path.join(os.path.realpath(os.path.dirname(__file__)), '..', '..', '')

    def _get_test_state_manager_path(self) -> str:
        return os.path.join(self._get_package_root_path(), 'tests', 'resources', '')

    def _get_absolute_path_from_state_manager(self, relative: str) -> str:
        return os.path.join(self._get_test_state_manager_path(), relative)

    def setup_method(self) -> None:
        from wexample_filestate.file_state_manager import FileStateManager

        self.state_manager = FileStateManager.create_from_path(
            path=self._get_test_state_manager_path(),
            options_providers=self._get_test_options_providers(),
            operations_providers=self._get_test_operations_providers(),
        )

    def _get_test_operations_providers(self) -> Optional[List[Type["AbstractOperationsProvider"]]]:
        return None

    def _get_test_options_providers(self) -> Optional[List[Type["AbstractOptionsProvider"]]]:
        return None

    def _assert_file_content_equals(self, file_path: str, expected_value: str, positive: bool = True):
        from wexample_helpers.helpers.file_helper import file_read

        assert (file_read(file_path) == expected_value) == positive
