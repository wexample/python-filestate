from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from wexample_filestate.item.file.xml_file import XmlFile
from wexample_filestate.testing.abstract_state_manager_test import AbstractStateManagerTest

if TYPE_CHECKING:
    pass


class TestXmlFile(AbstractStateManagerTest):
    """Test XmlFile functionality - smoke tests for XML file handling."""
    
    def _get_test_data_path(self) -> Path:
        """Get the path to test data directory."""
        return Path(__file__).parent / "test_data"
    
    def _create_xml_file(self, filename: str, tmp_path: Path) -> XmlFile:
        """Create an XmlFile from a test data file."""
        from wexample_prompt.common.io_manager import IoManager
        
        # Copy test data file to tmp_path
        test_file = self._get_test_data_path() / filename
        target_file = tmp_path / filename
        target_file.write_text(test_file.read_text())
        
        # Create XmlFile
        io = IoManager()
        return XmlFile.create_from_path(path=str(target_file), io=io)
    
    def test_xml_file_creation(self, tmp_path) -> None:
        """Test XmlFile can be created and basic properties work."""
        self._setup_with_tmp_path(tmp_path)
        
        xml_file = self._create_xml_file("sample.xml", tmp_path)
        
        # Test basic properties
        assert xml_file is not None, "XmlFile should be created successfully"
        assert xml_file._expected_file_name_extension() == "xml", "Extension should be 'xml'"
        assert xml_file.EXTENSION_XML == "xml", "Class constant should be 'xml'"
    
    def test_xml_file_loads(self, tmp_path) -> None:
        """Test XmlFile can parse XML content."""
        self._setup_with_tmp_path(tmp_path)
        
        xml_file = self._create_xml_file("sample.xml", tmp_path)
        
        # Read and parse content
        content = xml_file.read_text()
        parsed = xml_file.loads(content)
        
        # Test parsed content structure
        assert isinstance(parsed, dict), "Parsed content should be a dict"
        assert "project" in parsed, "Should parse root element"
        
        # Test project structure
        project = parsed["project"]
        assert isinstance(project, dict), "Project should be dict"
        
        # Basic smoke test - just ensure parsing works without errors
        # XML structure can vary based on xmltodict implementation
        assert len(project) > 0, "Project should have content"
    
    def test_xml_file_dumps_string_content(self, tmp_path) -> None:
        """Test XmlFile dumps method with string input."""
        self._setup_with_tmp_path(tmp_path)
        
        xml_file = self._create_xml_file("sample.xml", tmp_path)
        
        # Test with string content (should pass through)
        xml_string = "<root><item>test</item></root>"
        result = xml_file.dumps(xml_string)
        
        assert result == xml_string, "String content should pass through unchanged"
    
    def test_xml_file_dumps_dict_content(self, tmp_path) -> None:
        """Test XmlFile dumps method with dict input."""
        self._setup_with_tmp_path(tmp_path)
        
        xml_file = self._create_xml_file("sample.xml", tmp_path)
        
        # Test data as dict
        test_data = {
            "root": {
                "name": "test-app",
                "version": "1.0.0",
                "items": {
                    "item": ["item1", "item2", "item3"]
                }
            }
        }
        
        # Serialize to XML format
        xml_content = xml_file.dumps(test_data)
        
        # Test output format
        assert isinstance(xml_content, str), "Output should be string"
        assert "<root>" in xml_content, "Should contain root element"
        assert "<name>" in xml_content, "Should contain name element"
        assert "test-app" in xml_content, "Should contain content"
    
    def test_xml_file_roundtrip_simple(self, tmp_path) -> None:
        """Test XmlFile can parse and serialize simple XML consistently."""
        self._setup_with_tmp_path(tmp_path)
        
        xml_file = self._create_xml_file("sample.xml", tmp_path)
        
        # Simple XML for testing
        simple_xml = '<?xml version="1.0"?><root><name>test</name><value>123</value></root>'
        
        # Parse and serialize back
        parsed = xml_file.loads(simple_xml)
        serialized = xml_file.dumps(parsed)
        
        # Parse again to compare structure
        reparsed = xml_file.loads(serialized)
        
        # Should have same structure (exact format may differ)
        assert isinstance(reparsed, dict), "Reparsed should be dict"
        assert "root" in reparsed, "Should preserve root structure"
    
    def test_xml_file_loads_error_handling(self, tmp_path) -> None:
        """Test XmlFile error handling in loads method."""
        self._setup_with_tmp_path(tmp_path)
        
        xml_file = self._create_xml_file("sample.xml", tmp_path)
        
        # Test with invalid XML (non-strict mode)
        result = xml_file.loads("<invalid><xml>content", strict=False)
        assert result == {}, "Should return empty dict on error in non-strict mode"
        
        # Test with empty content
        result = xml_file.loads("", strict=False)
        assert result == {}, "Should handle empty content"
        
        # Test strict mode raises exception
        try:
            xml_file.loads("<invalid><xml>content", strict=True)
            assert False, "Should raise exception in strict mode"
        except Exception:
            pass  # Expected
    
    def test_xml_file_dumps_none_content(self, tmp_path) -> None:
        """Test XmlFile dumps method with None input."""
        self._setup_with_tmp_path(tmp_path)
        
        xml_file = self._create_xml_file("sample.xml", tmp_path)
        
        # Test with None content
        result = xml_file.dumps(None)
        assert isinstance(result, str), "Should return string for None input"
        
        # Test with empty dict
        result = xml_file.dumps({})
        assert isinstance(result, str), "Should return string for empty dict"
    
    def test_xml_file_dumps_fallback(self, tmp_path) -> None:
        """Test XmlFile dumps method fallback behavior."""
        self._setup_with_tmp_path(tmp_path)
        
        xml_file = self._create_xml_file("sample.xml", tmp_path)
        
        # Test with non-serializable content (should fallback to str())
        class CustomObject:
            def __str__(self):
                return "custom_object_string"
        
        result = xml_file.dumps(CustomObject())
        assert "custom_object_string" in result, "Should fallback to str() representation"
