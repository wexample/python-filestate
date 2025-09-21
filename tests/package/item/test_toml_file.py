from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from wexample_filestate.item.file.toml_file import TomlFile
from wexample_filestate.testing.abstract_state_manager_test import AbstractStateManagerTest

if TYPE_CHECKING:
    pass


class TestTomlFile(AbstractStateManagerTest):
    """Test TomlFile functionality - smoke tests for TOML file handling."""
    
    def _get_test_data_path(self) -> Path:
        """Get the path to test data directory."""
        return Path(__file__).parent / "test_data"
    
    def _create_toml_file(self, filename: str, tmp_path: Path) -> TomlFile:
        """Create a TomlFile from a test data file."""
        from wexample_prompt.common.io_manager import IoManager
        
        # Copy test data file to tmp_path
        test_file = self._get_test_data_path() / filename
        target_file = tmp_path / filename
        target_file.write_text(test_file.read_text())
        
        # Create TomlFile
        io = IoManager()
        return TomlFile.create_from_path(path=str(target_file), io=io)
    
    def test_toml_file_creation(self, tmp_path) -> None:
        """Test TomlFile can be created and basic properties work."""
        self._setup_with_tmp_path(tmp_path)
        
        toml_file = self._create_toml_file("sample.toml", tmp_path)
        
        # Test basic properties
        assert toml_file is not None, "TomlFile should be created successfully"
        assert toml_file._expected_file_name_extension() == "toml", "Extension should be 'toml'"
        assert toml_file.EXTENSION_TOML == "toml", "Class constant should be 'toml'"
    
    def test_toml_file_loads(self, tmp_path) -> None:
        """Test TomlFile can parse TOML content."""
        self._setup_with_tmp_path(tmp_path)
        
        toml_file = self._create_toml_file("sample.toml", tmp_path)
        
        # Read and parse content
        content = toml_file.read_text()
        parsed = toml_file.loads(content)
        
        # Test parsed content structure
        assert isinstance(parsed, dict), "Parsed content should be a dict"
        assert "project" in parsed, "Should parse project section"
        assert "dependencies" in parsed, "Should parse dependencies section"
        assert "scripts" in parsed, "Should parse scripts section"
        assert "config" in parsed, "Should parse config section"
        
        # Test project section
        project = parsed["project"]
        assert project["name"] == "test-project"
        assert project["version"] == "1.0.0"
        assert project["author"] == "Test Author"
        assert project["license"] == "MIT"
        
        # Test dependencies section
        deps = parsed["dependencies"]
        assert "express" in deps
        assert "lodash" in deps
        
        # Test config section with data types
        config = parsed["config"]
        assert config["debug"] is True, "Boolean values should be parsed correctly"
        assert config["port"] == 8000, "Integer values should be parsed correctly"
    
    def test_toml_file_dumps(self, tmp_path) -> None:
        """Test TomlFile can serialize dict to TOML format."""
        self._setup_with_tmp_path(tmp_path)
        
        toml_file = self._create_toml_file("sample.toml", tmp_path)
        
        # Test data
        test_data = {
            "app": {
                "name": "test-app",
                "version": "2.0.0"
            },
            "database": {
                "host": "localhost",
                "port": 5432,
                "ssl": True
            },
            "features": ["auth", "api", "ui"]
        }
        
        # Serialize to TOML format
        toml_content = toml_file.dumps(test_data)
        
        # Test output format
        assert isinstance(toml_content, str), "Output should be string"
        
        # Should be valid TOML that can be parsed back
        reparsed = toml_file.loads(toml_content)
        assert reparsed == test_data, "Serialized TOML should parse back to original data"
        
        # Test TOML formatting characteristics
        assert "[app]" in toml_content, "Should contain section headers"
        assert "[database]" in toml_content, "Should contain section headers"
        assert "name = " in toml_content, "Should contain key-value assignments"
    
    def test_toml_file_roundtrip(self, tmp_path) -> None:
        """Test TomlFile can parse and serialize consistently."""
        self._setup_with_tmp_path(tmp_path)
        
        toml_file = self._create_toml_file("sample.toml", tmp_path)
        
        # Read original content
        original_content = toml_file.read_text()
        
        # Parse and serialize back
        parsed = toml_file.loads(original_content)
        serialized = toml_file.dumps(parsed)
        
        # Parse again to compare
        reparsed = toml_file.loads(serialized)
        
        # Should have same structure and values
        assert parsed == reparsed, "Data should be preserved in roundtrip"
    
    def test_toml_file_loads_error_handling(self, tmp_path) -> None:
        """Test TomlFile error handling in loads method."""
        self._setup_with_tmp_path(tmp_path)
        
        toml_file = self._create_toml_file("sample.toml", tmp_path)
        
        # Test with invalid TOML (non-strict mode)
        result = toml_file.loads("[invalid toml content", strict=False)
        assert result == {}, "Should return empty dict on error in non-strict mode"
        
        # Test with empty content
        result = toml_file.loads("", strict=False)
        assert result == {}, "Should handle empty content"
        
        # Test strict mode raises exception
        try:
            toml_file.loads("[invalid toml content", strict=True)
            assert False, "Should raise exception in strict mode"
        except Exception:
            pass  # Expected
    
    def test_toml_file_dumps_none_content(self, tmp_path) -> None:
        """Test TomlFile dumps method with None input."""
        self._setup_with_tmp_path(tmp_path)
        
        toml_file = self._create_toml_file("sample.toml", tmp_path)
        
        # Test with None content
        result = toml_file.dumps(None)
        assert result == "", "Should return empty string for None input"
        
        # Test with empty dict
        result = toml_file.dumps({})
        assert result == "", "Should return empty string for empty dict"
    
    def test_toml_file_data_types(self, tmp_path) -> None:
        """Test TomlFile handles various data types correctly."""
        self._setup_with_tmp_path(tmp_path)
        
        toml_file = self._create_toml_file("sample.toml", tmp_path)
        
        # Test data with various types
        test_data = {
            "strings": {
                "basic": "hello world",
                "quoted": "hello \"world\""
            },
            "numbers": {
                "integer": 42,
                "float": 3.14
            },
            "booleans": {
                "true_val": True,
                "false_val": False
            },
            "arrays": {
                "simple": [1, 2, 3],
                "mixed": ["a", "b", "c"]
            }
        }
        
        # Serialize and parse back
        serialized = toml_file.dumps(test_data)
        reparsed = toml_file.loads(serialized)
        
        # Should preserve data types
        assert reparsed == test_data, "All data types should be preserved"
        assert isinstance(reparsed["numbers"]["integer"], int), "Integer should remain integer"
        assert isinstance(reparsed["numbers"]["float"], float), "Float should remain float"
        assert isinstance(reparsed["booleans"]["true_val"], bool), "Boolean should remain boolean"
