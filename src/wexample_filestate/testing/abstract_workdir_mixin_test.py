from __future__ import annotations

from typing import TYPE_CHECKING
from pathlib import Path

from wexample_filestate.testing.abstract_state_manager_test import AbstractStateManagerTest
from wexample_helpers.classes.abstract_method import abstract_method

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig
    from wexample_filestate.file_state_manager import FileStateManager


class AbstractWorkdirMixinTest(AbstractStateManagerTest):
    """Base class for testing workdir mixins."""
    
    def _setup_with_tmp_path(self, tmp_path) -> None:
        """Setup test with temporary path."""
        super()._setup_with_tmp_path(tmp_path)
        
    def _create_test_workdir_manager(self, tmp_path: Path) -> FileStateManager:
        """Create a test workdir manager that uses the mixin."""
        from wexample_filestate.file_state_manager import FileStateManager
        from wexample_prompt.common.io_manager import IoManager
        
        # Create the test class that inherits from the mixin
        TestWorkdirClass = self._get_test_workdir_class()
        
        # Create an instance with the mixin
        test_instance = TestWorkdirClass()
        
        # Create FileStateManager
        io = IoManager()
        manager = FileStateManager.create_from_path(
            path=str(tmp_path),
            config={},
            io=io
        )
        
        # Configure with mixin-specific config
        config = self._get_mixin_config()
        enhanced_config = self._apply_mixin_to_config(test_instance, config)
        manager.configure(config=enhanced_config)
        
        return manager
    
    @abstract_method
    def _get_test_workdir_class(self) -> type:
        """Return the test class that inherits from the mixin being tested."""
        pass
    
    @abstract_method
    def _get_mixin_config(self) -> DictConfig:
        """Return the base configuration for the mixin test."""
        pass
    
    @abstract_method
    def _apply_mixin_to_config(self, mixin_instance, config: DictConfig) -> DictConfig:
        """Apply the mixin method to enhance the config."""
        pass
    
    @abstract_method
    def _get_expected_files(self) -> list[str]:
        """Return list of files that should be created by the mixin."""
        pass
    
    def _assert_mixin_files_exist(self, tmp_path: Path, positive: bool = True) -> None:
        """Assert that mixin-created files exist or don't exist."""
        expected_files = self._get_expected_files()
        
        for filename in expected_files:
            file_path = tmp_path / filename
            if positive:
                assert file_path.exists(), f"Expected file {filename} to exist"
            else:
                assert not file_path.exists(), f"Expected file {filename} to not exist"
    
    def test_mixin_apply_and_rollback(self, tmp_path) -> None:
        """Test that mixin creates files on apply and removes them on rollback."""
        self._setup_with_tmp_path(tmp_path)
        
        # Create workdir manager with mixin
        manager = self._create_test_workdir_manager(tmp_path)
        
        # Initially files should not exist
        self._assert_mixin_files_exist(tmp_path, positive=False)
        
        # Apply - files should be created
        manager.apply()
        self._assert_mixin_files_exist(tmp_path, positive=True)
        
        # Rollback - files should be removed
        manager.rollback()
        self._assert_mixin_files_exist(tmp_path, positive=False)
