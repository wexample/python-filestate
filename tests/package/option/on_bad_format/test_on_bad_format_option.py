from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_test_operation import AbstractTestOperation

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class TestOnBadFormatOptionDelete(AbstractTestOperation):
    """Test OnBadFormatOption with delete action."""
    test_name: str = "INVALID_case.txt"

    def _operation_get_count(self) -> int:
        return 1  # Only delete operation (file creation is handled by should_exist)

    def _operation_test_assert_applied(self) -> None:
        # Verify the file was deleted due to invalid format
        file_path = self._get_absolute_path_from_state_manager(self.test_name)
        self._assert_file_exists(file_path=file_path, positive=False)

    def _operation_test_assert_initial(self) -> None:
        # No initial assertion needed - file will be created during setup
        pass

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.const.disk import DiskItemType

        return {
            "children": [
                {
                    "name": self.test_name,
                    "should_exist": True,
                    "type": DiskItemType.FILE,
                    "content": "test content",
                    "name_format": {
                        "case_format": "lowercase"
                    },
                    "on_bad_format": {
                        "action": "delete"
                    },
                }
            ]
        }


class TestOnBadFormatOptionRename(AbstractTestOperation):
    """Test OnBadFormatOption with rename action."""
    test_name: str = "INVALID_case.txt"
    expected_name: str = "invalid_case.txt"

    def _operation_get_count(self) -> int:
        return 1  # Only rename operation (file creation is handled by should_exist)

    def _operation_test_assert_applied(self) -> None:
        # Verify the file was renamed to correct format
        old_file_path = self._get_absolute_path_from_state_manager(self.test_name)
        new_file_path = self._get_absolute_path_from_state_manager(self.expected_name)
        
        self._assert_file_exists(file_path=old_file_path, positive=False)
        self._assert_file_exists(file_path=new_file_path, positive=True)

    def _operation_test_assert_initial(self) -> None:
        # No initial assertion needed - file will be created during setup
        pass

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.const.disk import DiskItemType

        return {
            "children": [
                {
                    "name": self.test_name,
                    "should_exist": True,
                    "type": DiskItemType.FILE,
                    "content": "test content",
                    "name_format": {
                        "case_format": "lowercase"
                    },
                    "on_bad_format": {
                        "action": "rename"
                    },
                }
            ]
        }


class TestOnBadFormatOptionIgnore(AbstractTestOperation):
    """Test OnBadFormatOption with ignore action."""
    test_name: str = "INVALID_case.txt"

    def _operation_get_count(self) -> int:
        return 0  # No operations should be created for ignore action

    def _operation_test_assert_applied(self) -> None:
        # Verify the file still exists (ignored the format violation)
        file_path = self._get_absolute_path_from_state_manager(self.test_name)
        self._assert_file_exists(file_path=file_path, positive=True)

    def _operation_test_assert_initial(self) -> None:
        # No initial assertion needed - file will be created during setup
        pass

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.const.disk import DiskItemType

        return {
            "children": [
                {
                    "name": self.test_name,
                    "should_exist": True,
                    "type": DiskItemType.FILE,
                    "content": "test content",
                    "name_format": {
                        "case_format": "lowercase"
                    },
                    "on_bad_format": {
                        "action": "ignore"
                    },
                }
            ]
        }
