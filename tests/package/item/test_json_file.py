from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from wexample_filestate.item.file.json_file import JsonFile
from wexample_filestate.testing.abstract_state_manager_test import AbstractStateManagerTest

if TYPE_CHECKING:
    pass


class TestJsonFile(AbstractStateManagerTest):
    """Test JsonFile functionality - smoke tests for JSON file handling."""
    
    def _get_test_data_path(self) -> Path:
        """Get the path to test data directory."""
        return Path(__file__).parent / "test_data"
    
    def _create_json_file(self, filename: str, tmp_path: Path) -> JsonFile:
        """Create a JsonFile from a test data file."""
        from wexample_prompt.common.io_manager import IoManager
        
        # Copy test data file to tmp_path
        test_file = self._get_test_data_path() / filename
        target_file = tmp_path / filename
        target_file.write_text(test_file.read_text())
        
        # Create JsonFile
        io = IoManager()
        return JsonFile.create_from_path(path=str(target_file), io=io)
    
    def test_json_file_creation(self, tmp_path) -> None:
        """Test JsonFile can be created and basic properties work."""
        self._setup_with_tmp_path(tmp_path)
        
        json_file = self._create_json_file("sample.json", tmp_path)
        
        # Test basic properties
        assert json_file is not None, "JsonFile should be created successfully"
        assert json_file._expected_file_name_extension() == "json", "Extension should be 'json'"
        assert json_file.EXTENSION_JSON == "json", "Class constant should be 'json'"
    
    def test_json_file_loads(self, tmp_path) -> None:
        """Test JsonFile can parse JSON content."""
        self._setup_with_tmp_path(tmp_path)
        
        json_file = self._create_json_file("sample.json", tmp_path)
        
        # Read and parse content
        content = json_file.read_text()
        parsed = json_file.loads(content)
        
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
        
        # Test nested objects
        assert isinstance(parsed["dependencies"], dict), "Dependencies should be dict"
        assert "express" in parsed["dependencies"]
        assert "lodash" in parsed["dependencies"]
        
        assert isinstance(parsed["scripts"], dict), "Scripts should be dict"
        assert "start" in parsed["scripts"]
        assert "test" in parsed["scripts"]
    
    def test_json_file_dumps(self, tmp_path) -> None:
        """Test JsonFile can serialize dict to JSON format."""
        self._setup_with_tmp_path(tmp_path)
        
        json_file = self._create_json_file("sample.json", tmp_path)
        
        # Test data
        test_data = {
            "name": "test-app",
            "version": "2.0.0",
            "config": {
                "debug": True,
                "port": 3000
            },
            "items": ["item1", "item2", "item3"]
        }
        
        # Serialize to JSON format
        json_content = json_file.dumps(test_data)
        
        # Test output format
        assert isinstance(json_content, str), "Output should be string"
        
        # Should be valid JSON
        reparsed = json.loads(json_content)
        assert reparsed == test_data, "Serialized JSON should parse back to original data"
        
        # Test formatting (should be indented)
        assert "  " in json_content, "Should be indented (pretty printed)"
        assert json_content.count("\n") > 1, "Should be multi-line formatted"
    
    def test_json_file_roundtrip(self, tmp_path) -> None:
        """Test JsonFile can parse and serialize consistently."""
        self._setup_with_tmp_path(tmp_path)
        
        json_file = self._create_json_file("sample.json", tmp_path)
        
        # Read original content
        original_content = json_file.read_text()
        
        # Parse and serialize back
        parsed = json_file.loads(original_content)
        serialized = json_file.dumps(parsed)
        
        # Parse again to compare
        reparsed = json_file.loads(serialized)
        
        # Should have same structure and values
        assert parsed == reparsed, "Data should be preserved in roundtrip"
    
    def test_json_file_loads_error_handling(self, tmp_path) -> None:
        """Test JsonFile error handling in loads method."""
        self._setup_with_tmp_path(tmp_path)
        
        json_file = self._create_json_file("sample.json", tmp_path)
        
        # Test with invalid JSON (non-strict mode)
        result = json_file.loads("{ invalid json }", strict=False)
        assert result == {}, "Should return empty dict on error in non-strict mode"
        
        # Test with empty content
        result = json_file.loads("", strict=False)
        assert result == {}, "Should handle empty content"
        
        # Test strict mode raises exception
        try:
            json_file.loads("{ invalid json }", strict=True)
            assert False, "Should raise exception in strict mode"
        except Exception:
            pass  # Expected
    
    def test_json_file_dumps_none_content(self, tmp_path) -> None:
        """Test JsonFile dumps method with None input."""
        self._setup_with_tmp_path(tmp_path)
        
        json_file = self._create_json_file("sample.json", tmp_path)
        
        # Test with None content
        result = json_file.dumps(None)
        assert result == "{}", "Should return empty JSON object for None input"
        
        # Should be valid JSON
        parsed = json.loads(result)
        assert parsed == {}, "Should parse to empty dict"
    
    def test_json_file_unicode_handling(self, tmp_path) -> None:
        """Test JsonFile handles Unicode characters correctly."""
        self._setup_with_tmp_path(tmp_path)
        
        json_file = self._create_json_file("sample.json", tmp_path)
        
        # Test data with Unicode
        test_data = {
            "name": "tést-àpp",
            "description": "Ünïcödé tëst 🚀",
            "emoji": "🎉✨🔥"
        }
        
        # Serialize and parse back
        serialized = json_file.dumps(test_data)
        reparsed = json_file.loads(serialized)
        
        # Should preserve Unicode characters
        assert reparsed == test_data, "Unicode characters should be preserved"
        assert "tést-àpp" in serialized, "Unicode should be in output"
        assert "🚀" in serialized, "Emoji should be in output"
