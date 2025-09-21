from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from wexample_filestate.item.file.env_file import EnvFile
from wexample_filestate.testing.abstract_state_manager_test import AbstractStateManagerTest

if TYPE_CHECKING:
    pass


class TestEnvFile(AbstractStateManagerTest):
    """Test EnvFile functionality - smoke tests for .env file handling."""
    
    def _get_test_data_path(self) -> Path:
        """Get the path to test data directory."""
        return Path(__file__).parent / "test_data"
    
    def _create_env_file(self, filename: str, tmp_path: Path) -> EnvFile:
        """Create an EnvFile from a test data file."""
        from wexample_prompt.common.io_manager import IoManager
        
        # Copy test data file to tmp_path
        test_file = self._get_test_data_path() / filename
        target_file = tmp_path / filename
        target_file.write_text(test_file.read_text())
        
        # Create EnvFile
        io = IoManager()
        return EnvFile.create_from_path(path=str(target_file), io=io)
    
    def test_env_file_creation(self, tmp_path) -> None:
        """Test EnvFile can be created and basic properties work."""
        self._setup_with_tmp_path(tmp_path)
        
        env_file = self._create_env_file("sample.env", tmp_path)
        
        # Test basic properties
        assert env_file is not None, "EnvFile should be created successfully"
        assert env_file._expected_file_name_extension() == "env", "Extension should be 'env'"
        assert env_file.EXTENSION_ENV == "env", "Class constant should be 'env'"
        assert env_file.EXTENSION_DOT_ENV == ".env", "Dot extension should be '.env'"
    
    def test_env_file_loads(self, tmp_path) -> None:
        """Test EnvFile can parse .env content."""
        self._setup_with_tmp_path(tmp_path)
        
        env_file = self._create_env_file("sample.env", tmp_path)
        
        # Read and parse content
        content = env_file.read_text()
        parsed = env_file.loads(content)
        
        # Test parsed content
        assert isinstance(parsed, dict), "Parsed content should be a dict"
        assert "DATABASE_URL" in parsed, "Should parse DATABASE_URL"
        assert "API_KEY" in parsed, "Should parse API_KEY"
        assert "DEBUG" in parsed, "Should parse DEBUG"
        assert "PORT" in parsed, "Should parse PORT"
        assert "SECRET_KEY" in parsed, "Should parse SECRET_KEY (even if empty)"
        
        # Test specific values
        assert parsed["DATABASE_URL"] == "postgresql://user:pass@localhost/db"
        assert parsed["API_KEY"] == "abc123"
        assert parsed["DEBUG"] == "true"
        assert parsed["PORT"] == "8000"
        assert parsed["SECRET_KEY"] == ""  # Empty value
    
    def test_env_file_dumps(self, tmp_path) -> None:
        """Test EnvFile can serialize dict to .env format."""
        self._setup_with_tmp_path(tmp_path)
        
        env_file = self._create_env_file("sample.env", tmp_path)
        
        # Test data
        test_data = {
            "APP_NAME": "test-app",
            "VERSION": "1.0.0",
            "DEBUG": "false",
            "EMPTY_VAR": None,
            "ANOTHER_VAR": ""
        }
        
        # Serialize to .env format
        env_content = env_file.dumps(test_data)
        
        # Test output format
        assert isinstance(env_content, str), "Output should be string"
        assert "APP_NAME=test-app" in env_content, "Should contain APP_NAME"
        assert "VERSION=1.0.0" in env_content, "Should contain VERSION"
        assert "DEBUG=false" in env_content, "Should contain DEBUG"
        assert "EMPTY_VAR=" in env_content, "Should handle None values as empty"
        assert "ANOTHER_VAR=" in env_content, "Should handle empty strings"
        assert env_content.endswith("\n"), "Should end with newline"
    
    def test_env_file_roundtrip(self, tmp_path) -> None:
        """Test EnvFile can parse and serialize consistently."""
        self._setup_with_tmp_path(tmp_path)
        
        env_file = self._create_env_file("sample.env", tmp_path)
        
        # Read original content
        original_content = env_file.read_text()
        
        # Parse and serialize back
        parsed = env_file.loads(original_content)
        serialized = env_file.dumps(parsed)
        
        # Parse again to compare
        reparsed = env_file.loads(serialized)
        
        # Should have same keys and values
        assert parsed.keys() == reparsed.keys(), "Keys should be preserved in roundtrip"
        for key in parsed:
            assert parsed[key] == reparsed[key], f"Value for {key} should be preserved"
    
    def test_env_file_loads_error_handling(self, tmp_path) -> None:
        """Test EnvFile error handling in loads method."""
        self._setup_with_tmp_path(tmp_path)
        
        env_file = self._create_env_file("sample.env", tmp_path)
        
        # Test with invalid content (non-strict mode)
        result = env_file.loads("invalid content that might cause issues", strict=False)
        assert isinstance(result, dict), "Should return empty dict on error in non-strict mode"
        
        # Test with empty content
        result = env_file.loads("", strict=False)
        assert isinstance(result, dict), "Should handle empty content"
    
    def test_env_file_dumps_non_dict(self, tmp_path) -> None:
        """Test EnvFile dumps method with non-dict input."""
        self._setup_with_tmp_path(tmp_path)
        
        env_file = self._create_env_file("sample.env", tmp_path)
        
        # Test with non-dict content
        result = env_file.dumps("not a dict")
        assert result == "", "Should return empty string for non-dict input"
        
        result = env_file.dumps(None)
        assert result == "", "Should return empty string for None input"
        
        result = env_file.dumps([1, 2, 3])
        assert result == "", "Should return empty string for list input"
