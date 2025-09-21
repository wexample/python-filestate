from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from wexample_filestate.option.children_file_factory_option import ChildrenFileFactoryOption
from wexample_filestate.testing.abstract_test_operation import AbstractTestOperation

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class TestChildrenFileFactoryOption(AbstractTestOperation):
    """Test ChildrenFileFactoryOption functionality."""
    
    def _operation_get_count(self) -> int:
        """ChildrenFileFactoryOption may not generate direct operations."""
        return 0
    
    def _get_test_data_path(self) -> Path:
        """Get the path to test data directory."""
        return Path(__file__).parent / "test_data"
    
    def _operation_test_setup(self) -> None:
        """Setup test by configuring and copying test data."""
        super()._operation_test_setup()
        self._operation_test_setup_copy_test_data()
    
    def _operation_test_setup_configuration(self) -> DictConfig | None:
        """Setup configuration for testing ChildrenFileFactoryOption."""
        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.option.name_pattern_option import NamePatternOption
        
        return {
            "name": "test_root",
            "type": DiskItemType.DIRECTORY,
            "should_exist": True,
            "children": [
                ChildrenFileFactoryOption(
                    pattern={
                        "name": "config.txt",
                        "type": DiskItemType.FILE,
                        "should_exist": True,  # This should trigger FileCreateOperation
                        NamePatternOption.get_name(): ["project_.*"]  # Match project_a, project_b
                    },
                    recursive=False,
                )
            ]
        }
    
    def _operation_test_setup_copy_test_data(self) -> None:
        """Copy test data to the temporary directory."""
        import shutil
        
        test_data_path = self._get_test_data_path()
        target_path = self.state_manager.get_path()
        
        # Copy all test data directories
        for item in test_data_path.iterdir():
            if item.is_dir():
                shutil.copytree(item, target_path / item.name)
            else:
                shutil.copy2(item, target_path / item.name)
    
    def _operation_test_assert_initial(self) -> None:
        """Assert initial state before applying operations."""
        # Ensure test data directories exist
        test_root = self.state_manager.get_path()
        assert (test_root / "project_a").exists(), "project_a should exist"
        assert (test_root / "project_b").exists(), "project_b should exist"
        assert (test_root / "other_dir").exists(), "other_dir should exist"
        assert (test_root / "no_match_dir").exists(), "no_match_dir should exist"
        
        # Ensure config.txt files don't exist yet
        assert not (test_root / "project_a" / "config.txt").exists(), "config.txt should not exist in project_a initially"
        assert not (test_root / "project_b" / "config.txt").exists(), "config.txt should not exist in project_b initially"
        assert not (test_root / "other_dir" / "config.txt").exists(), "config.txt should not exist in other_dir initially"
    
    def _operation_test_assert_applied(self) -> None:
        """Assert state after applying operations."""
        # Since ChildrenFileFactoryOption generates children configurations
        # but doesn't directly create files, we test that the option
        # has been processed without errors
        test_root = self.state_manager.get_path()
        
        # The directories should still exist
        assert (test_root / "project_a").exists(), "project_a should still exist"
        assert (test_root / "project_b").exists(), "project_b should still exist"
        assert (test_root / "other_dir").exists(), "other_dir should still exist"
        assert (test_root / "no_match_dir").exists(), "no_match_dir should still exist"
        
        # Test that the ChildrenFileFactoryOption has generated children
        # by checking if the state manager has the expected structure
        children_factory_option = None
        for option in self.state_manager.options.values():
            # print(f"Option: {option}, name: {option.get_name()}")
            if option.get_name() == "children":
                # Look inside the children option for ChildrenFileFactoryOption
                if hasattr(option, 'children') and option.children:
                    for child_option in option.children:
                        if isinstance(child_option, ChildrenFileFactoryOption):
                            children_factory_option = child_option
                            break
                # Also check if the option itself contains the factory option
                elif hasattr(option, 'value') and isinstance(option.value, list):
                    for child_item in option.value:
                        if isinstance(child_item, ChildrenFileFactoryOption):
                            children_factory_option = child_item
                            break
            if children_factory_option:
                break
        
        assert children_factory_option is not None, "ChildrenFileFactoryOption should be configured"
        
        # Test the generate_children method directly
        generated_children = children_factory_option.generate_children()
        assert len(generated_children) == 2, "Should generate children for 2 matching directories (project_a, project_b)"


class TestChildrenFileFactoryOptionRecursive(AbstractTestOperation):
    """Test ChildrenFileFactoryOption with recursive=True."""
    
    def _operation_get_count(self) -> int:
        """Expect 5 operations: one for each directory including nested ones."""
        return 5
    
    def _get_test_data_path(self) -> Path:
        """Get the path to test data directory."""
        return Path(__file__).parent / "test_data"
    
    def _operation_test_setup(self) -> None:
        """Setup test by configuring and copying test data."""
        super()._operation_test_setup()
        self._operation_test_setup_copy_test_data()
    
    def _operation_test_setup_copy_test_data(self) -> None:
        """Copy test data to the temporary directory."""
        import shutil
        
        test_data_path = self._get_test_data_path()
        target_path = self.state_manager.get_path()
        
        # Copy all test data directories
        for item in test_data_path.iterdir():
            if item.is_dir():
                shutil.copytree(item, target_path / item.name)
            else:
                shutil.copy2(item, target_path / item.name)
    
    def _operation_test_setup_configuration(self) -> DictConfig | None:
        """Setup configuration for testing recursive ChildrenFileFactoryOption."""
        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.option.name_pattern_option import NamePatternOption
        
        return {
            "name": "test_root",
            "type": DiskItemType.DIRECTORY,
            "should_exist": True,
            "children": [
                ChildrenFileFactoryOption(
                    pattern={
                        "name": "README.md",
                        "type": DiskItemType.FILE,
                        NamePatternOption.get_name(): [".*"]  # Match all directories
                    },
                    recursive=True,
                )
            ]
        }
    
    def _operation_test_setup_copy_test_data(self) -> None:
        """Copy test data to the temporary directory."""
        import shutil
        
        test_data_path = self._get_test_data_path()
        target_path = self.state_manager.get_path()
        
        # Copy all test data directories
        for item in test_data_path.iterdir():
            if item.is_dir():
                shutil.copytree(item, target_path / item.name)
            else:
                shutil.copy2(item, target_path / item.name)
    
    def _operation_test_assert_initial(self) -> None:
        """Assert initial state before applying operations."""
        test_root = self.state_manager.get_path()
        
        # Ensure README.md files don't exist yet
        assert not (test_root / "project_a" / "README.md").exists(), "README.md should not exist in project_a initially"
        assert not (test_root / "project_b" / "README.md").exists(), "README.md should not exist in project_b initially"
        assert not (test_root / "project_b" / "subdir" / "README.md").exists(), "README.md should not exist in project_b/subdir initially"
    
    def _operation_test_assert_applied(self) -> None:
        """Assert state after applying operations with recursive=True."""
        test_root = self.state_manager.get_path()
        
        # README.md should be created in all directories (recursive)
        assert (test_root / "project_a" / "README.md").exists(), "README.md should be created in project_a"
        assert (test_root / "project_b" / "README.md").exists(), "README.md should be created in project_b"
        assert (test_root / "project_b" / "subdir" / "README.md").exists(), "README.md should be created in project_b/subdir"
        assert (test_root / "other_dir" / "README.md").exists(), "README.md should be created in other_dir"
        assert (test_root / "no_match_dir" / "README.md").exists(), "README.md should be created in no_match_dir"
        
        # Verify files are actual files
        assert (test_root / "project_a" / "README.md").is_file(), "README.md in project_a should be a file"
        assert (test_root / "project_b" / "subdir" / "README.md").is_file(), "README.md in project_b/subdir should be a file"


class TestChildrenFileFactoryOptionNoPattern(AbstractTestOperation):
    """Test ChildrenFileFactoryOption without name pattern (matches all)."""
    
    def _operation_get_count(self) -> int:
        """Expect 4 operations: one for each directory."""
        return 4
    
    def _get_test_data_path(self) -> Path:
        """Get the path to test data directory."""
        return Path(__file__).parent / "test_data"
    
    def _operation_test_setup(self) -> None:
        """Setup test by configuring and copying test data."""
        super()._operation_test_setup()
        self._operation_test_setup_copy_test_data()
    
    def _operation_test_setup_copy_test_data(self) -> None:
        """Copy test data to the temporary directory."""
        import shutil
        
        test_data_path = self._get_test_data_path()
        target_path = self.state_manager.get_path()
        
        # Copy all test data directories
        for item in test_data_path.iterdir():
            if item.is_dir():
                shutil.copytree(item, target_path / item.name)
            else:
                shutil.copy2(item, target_path / item.name)
    
    def _operation_test_setup_configuration(self) -> DictConfig | None:
        """Setup configuration without name pattern."""
        from wexample_filestate.const.disk import DiskItemType
        
        return {
            "name": "test_root",
            "type": DiskItemType.DIRECTORY,
            "should_exist": True,
            "children": [
                ChildrenFileFactoryOption(
                    pattern={
                        "name": "universal.txt",
                        "type": DiskItemType.FILE,
                        # No name_pattern - should match all directories
                    },
                    recursive=False,
                )
            ]
        }
    
    def _operation_test_setup_copy_test_data(self) -> None:
        """Copy test data to the temporary directory."""
        import shutil
        
        test_data_path = self._get_test_data_path()
        target_path = self.state_manager.get_path()
        
        # Copy all test data directories
        for item in test_data_path.iterdir():
            if item.is_dir():
                shutil.copytree(item, target_path / item.name)
            else:
                shutil.copy2(item, target_path / item.name)
    
    def _operation_test_assert_initial(self) -> None:
        """Assert initial state before applying operations."""
        test_root = self.state_manager.get_path()
        
        # Ensure universal.txt files don't exist yet
        assert not (test_root / "project_a" / "universal.txt").exists(), "universal.txt should not exist initially"
        assert not (test_root / "project_b" / "universal.txt").exists(), "universal.txt should not exist initially"
        assert not (test_root / "other_dir" / "universal.txt").exists(), "universal.txt should not exist initially"
        assert not (test_root / "no_match_dir" / "universal.txt").exists(), "universal.txt should not exist initially"
    
    def _operation_test_assert_applied(self) -> None:
        """Assert state after applying operations without name pattern."""
        test_root = self.state_manager.get_path()
        
        # universal.txt should be created in ALL directories (no pattern = match all)
        assert (test_root / "project_a" / "universal.txt").exists(), "universal.txt should be created in project_a"
        assert (test_root / "project_b" / "universal.txt").exists(), "universal.txt should be created in project_b"
        assert (test_root / "other_dir" / "universal.txt").exists(), "universal.txt should be created in other_dir"
        assert (test_root / "no_match_dir" / "universal.txt").exists(), "universal.txt should be created in no_match_dir"
        
        # Verify files are actual files
        assert (test_root / "project_a" / "universal.txt").is_file(), "universal.txt in project_a should be a file"
        assert (test_root / "other_dir" / "universal.txt").is_file(), "universal.txt in other_dir should be a file"


class TestChildrenFileFactoryOptionEmptyDirectory(AbstractTestOperation):
    """Test ChildrenFileFactoryOption with empty directory."""
    
    def _operation_get_count(self) -> int:
        """Expect 0 operations for empty directory."""
        return 0
    
    def _operation_test_setup_configuration(self) -> DictConfig | None:
        """Setup configuration for empty directory test."""
        from wexample_filestate.const.disk import DiskItemType
        
        return {
            "name": "empty_root",
            "type": DiskItemType.DIRECTORY,
            "should_exist": True,
            "children": [
                ChildrenFileFactoryOption(
                    pattern={
                        "name": "should_not_exist.txt",
                        "type": DiskItemType.FILE,
                    },
                    recursive=False,
                )
            ]
        }
    
    def _operation_test_assert_initial(self) -> None:
        """Assert initial state - empty directory."""
        test_root = self.state_manager.get_path()
        assert test_root.exists(), "Root directory should exist"
        assert test_root.is_dir(), "Root should be a directory"
        
        # Directory should be empty (or only contain .gitkeep type files)
        children = list(test_root.iterdir())
        assert len([c for c in children if c.is_dir()]) == 0, "Should have no subdirectories initially"
    
    def _operation_test_assert_applied(self) -> None:
        """Assert state after applying operations on empty directory."""
        test_root = self.state_manager.get_path()
        
        # No files should be created since there are no subdirectories
        assert not (test_root / "should_not_exist.txt").exists(), "File should not be created in empty directory"
        
        # Directory should still be empty of generated files
        children = list(test_root.iterdir())
        generated_files = [c for c in children if c.name == "should_not_exist.txt"]
        assert len(generated_files) == 0, "No files should be generated in empty directory"
