from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from wexample_filestate.item.file.yaml_file import YamlFile
from wexample_filestate.testing.abstract_state_manager_test import AbstractStateManagerTest

if TYPE_CHECKING:
    pass


class TestYamlFile(AbstractStateManagerTest):
    """Test YamlFile functionality - smoke tests for YAML file handling."""
    
    def _get_test_data_path(self) -> Path:
        """Get the path to test data directory."""
        return Path(__file__).parent / "test_data"
    
    def _create_yaml_file(self, filename: str, tmp_path: Path) -> YamlFile:
        """Create a YamlFile from a test data file."""
        from wexample_prompt.common.io_manager import IoManager
        
        # Copy test data file to tmp_path
        test_file = self._get_test_data_path() / filename
        target_file = tmp_path / filename
        target_file.write_text(test_file.read_text())
        
        # Create YamlFile
        io = IoManager()
        return YamlFile.create_from_path(path=str(target_file), io=io)
    
    def test_yaml_file_creation(self, tmp_path) -> None:
        """Test YamlFile can be created and basic properties work."""
        self._setup_with_tmp_path(tmp_path)
        
        yaml_file = self._create_yaml_file("sample.yaml", tmp_path)
        
        # Test basic properties
        assert yaml_file is not None, "YamlFile should be created successfully"
        assert yaml_file._expected_file_name_extension() == "yml", "Extension should be 'yml'"
        assert yaml_file.EXTENSION_YML == "yml", "Class constant should be 'yml'"
    
    def test_yaml_file_loads(self, tmp_path) -> None:
        """Test YamlFile can parse YAML content."""
        self._setup_with_tmp_path(tmp_path)
        
        yaml_file = self._create_yaml_file("sample.yaml", tmp_path)
        
        # Read and parse content
        content = yaml_file.read_text()
        parsed = yaml_file.loads(content)
        
        # Test parsed content structure
        assert isinstance(parsed, dict), "Parsed content should be a dict"
        assert "name" in parsed, "Should parse name field"
        assert "version" in parsed, "Should parse version field"
        assert "dependencies" in parsed, "Should parse dependencies field"
        assert "scripts" in parsed, "Should parse scripts field"
        
        # Test specific values
        assert parsed["name"] == "test-project"
        assert parsed["version"] == "1.0.0"
        assert parsed["author"] == "Test Author"
        assert parsed["license"] == "MIT"
        
        # Test nested structures
        assert isinstance(parsed["dependencies"], list), "Dependencies should be list"
        assert len(parsed["dependencies"]) == 2, "Should have 2 dependencies"
        
        assert isinstance(parsed["scripts"], dict), "Scripts should be dict"
        assert "start" in parsed["scripts"]
        assert "test" in parsed["scripts"]
        
        assert isinstance(parsed["config"], dict), "Config should be dict"
        assert parsed["config"]["debug"] is True, "Boolean values should be parsed correctly"
        assert parsed["config"]["port"] == 8000, "Integer values should be parsed correctly"
    
    def test_yaml_file_dumps(self, tmp_path) -> None:
        """Test YamlFile can serialize dict to YAML format."""
        self._setup_with_tmp_path(tmp_path)
        
        yaml_file = self._create_yaml_file("sample.yaml", tmp_path)
        
        # Test data
        test_data = {
            "name": "test-app",
            "version": "2.0.0",
            "config": {
                "debug": True,
                "port": 3000,
                "features": ["auth", "api", "ui"]
            },
            "items": ["item1", "item2", "item3"]
        }
        
        # Serialize to YAML format
        yaml_content = yaml_file.dumps(test_data)
        
        # Test output format
        assert isinstance(yaml_content, str), "Output should be string"
        
        # Should be valid YAML that can be parsed back
        reparsed = yaml_file.loads(yaml_content)
        assert reparsed == test_data, "Serialized YAML should parse back to original data"
        
        # Test YAML formatting characteristics
        assert "name: test-app" in yaml_content, "Should contain key-value pairs"
        assert "- item1" in yaml_content, "Should format lists with dashes"
    
    def test_yaml_file_roundtrip(self, tmp_path) -> None:
        """Test YamlFile can parse and serialize consistently."""
        self._setup_with_tmp_path(tmp_path)
        
        yaml_file = self._create_yaml_file("sample.yaml", tmp_path)
        
        # Read original content
        original_content = yaml_file.read_text()
        
        # Parse and serialize back
        parsed = yaml_file.loads(original_content)
        serialized = yaml_file.dumps(parsed)
        
        # Parse again to compare
        reparsed = yaml_file.loads(serialized)
        
        # Should have same structure and values
        assert parsed == reparsed, "Data should be preserved in roundtrip"
    
    def test_yaml_file_loads_error_handling(self, tmp_path) -> None:
        """Test YamlFile error handling in loads method."""
        self._setup_with_tmp_path(tmp_path)
        
        yaml_file = self._create_yaml_file("sample.yaml", tmp_path)
        
        # Test with invalid YAML (non-strict mode)
        result = yaml_file.loads("{ invalid: yaml: content }", strict=False)
        assert result == {}, "Should return empty dict on error in non-strict mode"
        
        # Test with empty content
        result = yaml_file.loads("", strict=False)
        assert result == {}, "Should handle empty content"
        
        # Test strict mode raises exception
        try:
            yaml_file.loads("{ invalid: yaml: content }", strict=True)
            assert False, "Should raise exception in strict mode"
        except Exception:
            pass  # Expected
    
    def test_yaml_file_dumps_none_content(self, tmp_path) -> None:
        """Test YamlFile dumps method with None input."""
        self._setup_with_tmp_path(tmp_path)
        
        yaml_file = self._create_yaml_file("sample.yaml", tmp_path)
        
        # Test with None content
        result = yaml_file.dumps(None)
        assert result == "{}\n", "Should return empty YAML object for None input"
        
        # Should be valid YAML
        parsed = yaml_file.loads(result)
        assert parsed == {}, "Should parse to empty dict"
    
    def test_yaml_file_data_types(self, tmp_path) -> None:
        """Test YamlFile handles various data types correctly."""
        self._setup_with_tmp_path(tmp_path)
        
        yaml_file = self._create_yaml_file("sample.yaml", tmp_path)
        
        # Test data with various types
        test_data = {
            "string": "hello world",
            "integer": 42,
            "float": 3.14,
            "boolean_true": True,
            "boolean_false": False,
            "null_value": None,
            "list": [1, 2, 3],
            "nested_dict": {
                "inner": "value"
            }
        }
        
        # Serialize and parse back
        serialized = yaml_file.dumps(test_data)
        reparsed = yaml_file.loads(serialized)
        
        # Should preserve data types
        assert reparsed == test_data, "All data types should be preserved"
        assert isinstance(reparsed["integer"], int), "Integer should remain integer"
        assert isinstance(reparsed["float"], float), "Float should remain float"
        assert isinstance(reparsed["boolean_true"], bool), "Boolean should remain boolean"
        assert reparsed["null_value"] is None, "None should remain None"
