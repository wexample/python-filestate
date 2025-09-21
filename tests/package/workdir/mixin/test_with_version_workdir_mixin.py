from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_workdir_mixin_test import AbstractWorkdirMixinTest
from wexample_filestate.workdir.mixin.with_version_workdir_mixin import WithVersionWorkdirMixin
from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


@base_class
class TestVersionWorkdir(WithVersionWorkdirMixin, BaseClass):
    """Test class that inherits from WithVersionWorkdirMixin."""
    pass


class TestWithVersionWorkdirMixin(AbstractWorkdirMixinTest):
    """Test WithVersionWorkdirMixin functionality."""
    
    def _get_test_workdir_class(self) -> type:
        """Return the test class that inherits from WithVersionWorkdirMixin."""
        return TestVersionWorkdir
    
    def _get_mixin_config(self) -> DictConfig:
        """Return the base configuration for the version mixin test."""
        return {
            "children": []
        }
    
    def _apply_mixin_to_config(self, mixin_instance: TestVersionWorkdir, config: DictConfig) -> DictConfig:
        """Apply the version mixin method to enhance the config."""
        return mixin_instance.append_version(config)
    
    def _get_expected_files(self) -> list[str]:
        """Return list of files that should be created by the version mixin."""
        return ["version.txt"]
    
    def _get_apply_count(self) -> int:
        """Version mixin needs 2 applies: 1 for file creation, 1 for content writing."""
        return 2
    
    def test_version_content(self, tmp_path) -> None:
        """Test that version.txt contains the expected default version."""
        from wexample_helpers.const.version import DEFAULT_VERSION_NUMBER
        from wexample_helpers.helpers.file import file_read
        
        self._setup_with_tmp_path(tmp_path)
        
        # Create workdir manager with version mixin
        manager = self._create_test_workdir_manager(tmp_path)
        
        # Apply multiple times to fully create and populate version.txt
        apply_count = self._get_apply_count()
        for i in range(apply_count):
            manager.apply()
        
        # Check version.txt content
        version_file = tmp_path / "version.txt"
        content = file_read(version_file)
        
        # Should contain default version with newline
        expected_content = f"{DEFAULT_VERSION_NUMBER}\n"
        assert content == expected_content, f"Expected '{expected_content}', got '{content}'"
