from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeVar

from wexample_filestate.item.file.structured_content_file import StructuredContentFile
from wexample_filestate.testing.abstract_state_manager_test import AbstractStateManagerTest

if TYPE_CHECKING:
    pass

# Type variable for the specific file type (JsonFile, YamlFile, etc.)
FileType = TypeVar('FileType', bound=StructuredContentFile)


class AbstractStructuredFileTest(AbstractStateManagerTest, ABC):
    """Abstract base class for testing structured file types (JSON, YAML, TOML, XML).
    
    This class provides common functionality for testing files that can be parsed
    into structured data (dicts, lists) and serialized back to text format.
    """
    
    def _get_test_data_path(self) -> Path:
        """Get the path to test data directory."""
        # Navigate from src/wexample_filestate/testing/ to tests/package/item/test_data/
        return Path(__file__).parent.parent.parent.parent / "tests" / "package" / "item" / "test_data"
    
    @abstractmethod
    def _get_file_class(self) -> type[FileType]:
        """Get the file class to test (e.g., JsonFile, YamlFile)."""
        pass
    
    @abstractmethod
    def _get_expected_extension(self) -> str:
        """Get the expected file extension (e.g., 'json', 'yml')."""
        pass
    
    @abstractmethod
    def _get_extension_constant_name(self) -> str:
        """Get the extension constant name (e.g., 'EXTENSION_JSON')."""
        pass
    
    @abstractmethod
    def _get_sample_filename(self) -> str:
        """Get the sample test file name (e.g., 'sample.json')."""
        pass
    
    @abstractmethod
    def _get_file_type_name(self) -> str:
        """Get the file type name for messages (e.g., 'JsonFile', 'YamlFile')."""
        pass
    
    def _create_file(self, filename: str, tmp_path: Path) -> FileType:
        """Create a file instance from a test data file."""
        from wexample_prompt.common.io_manager import IoManager
        
        # Copy test data file to tmp_path
        test_file = self._get_test_data_path() / filename
        target_file = tmp_path / filename
        target_file.write_text(test_file.read_text())
        
        # Create file instance
        io = IoManager()
        file_class = self._get_file_class()
        return file_class.create_from_path(path=str(target_file), io=io)
    
    def test_file_creation(self, tmp_path) -> None:
        """Test file can be created and basic properties work."""
        self._setup_with_tmp_path(tmp_path)
        
        file_instance = self._create_file(self._get_sample_filename(), tmp_path)
        
        # Test basic properties
        file_type_name = self._get_file_type_name()
        assert file_instance is not None, f"{file_type_name} should be created successfully"
        
        expected_ext = self._get_expected_extension()
        assert file_instance._expected_file_name_extension() == expected_ext, f"Extension should be '{expected_ext}'"
        
        # Test extension constant
        constant_name = self._get_extension_constant_name()
        assert hasattr(file_instance, constant_name), f"Should have {constant_name} constant"
        constant_value = getattr(file_instance, constant_name)
        assert constant_value == expected_ext, f"Class constant should be '{expected_ext}'"
    
    def test_file_loads(self, tmp_path) -> None:
        """Test file can parse content into structured data."""
        self._setup_with_tmp_path(tmp_path)
        
        file_instance = self._create_file(self._get_sample_filename(), tmp_path)
        
        # Read and parse content
        content = file_instance.read_text()
        parsed = file_instance.loads(content)
        
        # Test parsed content structure
        assert isinstance(parsed, dict), "Parsed content should be a dict"
        
        # Validate common structure expected in test files
        self._validate_parsed_content(parsed)
    
    def test_file_dumps(self, tmp_path) -> None:
        """Test file can serialize structured data to text format."""
        self._setup_with_tmp_path(tmp_path)
        
        file_instance = self._create_file(self._get_sample_filename(), tmp_path)
        
        # Test data
        test_data = self._get_test_data_for_dumps()
        
        # Serialize to text format
        serialized_content = file_instance.dumps(test_data)
        
        # Test output format
        assert isinstance(serialized_content, str), "Output should be string"
        assert len(serialized_content) > 0, "Output should not be empty"
        
        # Test round-trip: serialize then parse should give back original data
        parsed_back = file_instance.loads(serialized_content)
        self._assert_roundtrip_equality(test_data, parsed_back)
    
    def test_file_roundtrip_consistency(self, tmp_path) -> None:
        """Test that loading and dumping preserves data integrity."""
        self._setup_with_tmp_path(tmp_path)
        
        file_instance = self._create_file(self._get_sample_filename(), tmp_path)
        
        # Load original content
        original_content = file_instance.read_text()
        parsed_data = file_instance.loads(original_content)
        
        # Dump and reload
        serialized_content = file_instance.dumps(parsed_data)
        reparsed_data = file_instance.loads(serialized_content)
        
        # Data should be preserved through the roundtrip
        self._assert_roundtrip_equality(parsed_data, reparsed_data)
    
    def _validate_parsed_content(self, parsed: dict) -> None:
        """Validate the structure of parsed content from sample file.
        
        Override this method to add specific validations for your file type.
        """
        # Default validation - can be overridden by subclasses
        assert "name" in parsed, "Should parse name field"
        assert "version" in parsed, "Should parse version field"
    
    def _get_test_data_for_dumps(self) -> dict[str, Any]:
        """Get test data for dumps test.
        
        Override this method to provide specific test data for your file type.
        """
        return {
            "name": "test-app",
            "version": "2.0.0",
            "config": {
                "debug": True,
                "port": 3000
            },
            "items": ["item1", "item2", "item3"]
        }
    
    def _assert_roundtrip_equality(self, original: Any, roundtrip: Any) -> None:
        """Assert that original and roundtrip data are equal.
        
        Override this method if your file format has specific equality requirements.
        """
        assert original == roundtrip, "Roundtrip should preserve data exactly"
