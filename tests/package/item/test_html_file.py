from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from wexample_filestate.item.file.html_file import HtmlFile
from wexample_filestate.testing.abstract_state_manager_test import AbstractStateManagerTest

if TYPE_CHECKING:
    pass


class TestHtmlFile(AbstractStateManagerTest):
    """Test HtmlFile functionality - smoke tests for HTML file handling."""
    
    def _get_test_data_path(self) -> Path:
        """Get the path to test data directory."""
        return Path(__file__).parent / "test_data"
    
    def _create_html_file(self, filename: str, tmp_path: Path) -> HtmlFile:
        """Create an HtmlFile from a test data file."""
        from wexample_prompt.common.io_manager import IoManager
        
        # Copy test data file to tmp_path
        test_file = self._get_test_data_path() / filename
        target_file = tmp_path / filename
        target_file.write_text(test_file.read_text())
        
        # Create HtmlFile
        io = IoManager()
        return HtmlFile.create_from_path(path=str(target_file), io=io)
    
    def test_html_file_creation(self, tmp_path) -> None:
        """Test HtmlFile can be created and basic properties work."""
        self._setup_with_tmp_path(tmp_path)
        
        html_file = self._create_html_file("sample.html", tmp_path)
        
        # Test basic properties
        assert html_file is not None, "HtmlFile should be created successfully"
        assert html_file._expected_file_name_extension() == "html", "Extension should be 'html'"
        assert html_file.EXTENSION_HTML == "html", "Class constant should be 'html'"
        assert html_file.EXTENSION_HTM == "htm", "HTM constant should be 'htm'"
    
    def test_html_file_loads(self, tmp_path) -> None:
        """Test HtmlFile loads method (returns raw HTML string)."""
        self._setup_with_tmp_path(tmp_path)
        
        html_file = self._create_html_file("sample.html", tmp_path)
        
        # Read and "parse" content (actually just returns the string)
        content = html_file.read_text()
        parsed = html_file.loads(content)
        
        # HtmlFile.loads() just returns the raw string
        assert isinstance(parsed, str), "Parsed content should be a string"
        assert parsed == content, "Loads should return the original content unchanged"
        
        # Test that HTML content is preserved
        assert "<!DOCTYPE html>" in parsed, "Should preserve DOCTYPE"
        assert "<html" in parsed, "Should preserve HTML tag"
        assert "<head>" in parsed, "Should preserve head section"
        assert "<body>" in parsed, "Should preserve body section"
        assert "Welcome to Test Project" in parsed, "Should preserve content"
    
    def test_html_file_dumps_string_content(self, tmp_path) -> None:
        """Test HtmlFile dumps method with string input."""
        self._setup_with_tmp_path(tmp_path)
        
        html_file = self._create_html_file("sample.html", tmp_path)
        
        # Test with string content (should pass through)
        html_string = "<html><body><h1>Test</h1></body></html>"
        result = html_file.dumps(html_string)
        
        assert result == html_string, "String content should pass through unchanged"
        assert isinstance(result, str), "Result should be string"
    
    def test_html_file_dumps_object_content(self, tmp_path) -> None:
        """Test HtmlFile dumps method with object input."""
        self._setup_with_tmp_path(tmp_path)
        
        html_file = self._create_html_file("sample.html", tmp_path)
        
        # Test with object that has __str__ method
        class MockHtmlObject:
            def __str__(self):
                return "<div>Generated HTML</div>"
        
        html_obj = MockHtmlObject()
        result = html_file.dumps(html_obj)
        
        assert result == "<div>Generated HTML</div>", "Should convert object to string"
        assert isinstance(result, str), "Result should be string"
    
    def test_html_file_roundtrip(self, tmp_path) -> None:
        """Test HtmlFile can load and dump consistently."""
        self._setup_with_tmp_path(tmp_path)
        
        html_file = self._create_html_file("sample.html", tmp_path)
        
        # Read original content
        original_content = html_file.read_text()
        
        # Load and dump back
        loaded = html_file.loads(original_content)
        dumped = html_file.dumps(loaded)
        
        # Should be identical since both operations are pass-through
        assert loaded == original_content, "Loads should return original content"
        assert dumped == original_content, "Dumps should return original content"
        assert loaded == dumped, "Roundtrip should preserve content exactly"
    
    def test_html_file_loads_error_handling(self, tmp_path) -> None:
        """Test HtmlFile loads method with various inputs."""
        self._setup_with_tmp_path(tmp_path)
        
        html_file = self._create_html_file("sample.html", tmp_path)
        
        # HtmlFile.loads() doesn't actually parse, so it should handle any string
        result = html_file.loads("invalid html content")
        assert result == "invalid html content", "Should return input unchanged"
        
        # Test with empty content
        result = html_file.loads("")
        assert result == "", "Should handle empty content"
        
        # Test with malformed HTML
        malformed = "<html><body><div>unclosed div<p>unclosed p"
        result = html_file.loads(malformed)
        assert result == malformed, "Should return malformed HTML unchanged"
    
    def test_html_file_dumps_none_content(self, tmp_path) -> None:
        """Test HtmlFile dumps method with None input."""
        self._setup_with_tmp_path(tmp_path)
        
        html_file = self._create_html_file("sample.html", tmp_path)
        
        # Test with None content
        result = html_file.dumps(None)
        assert result == "", "Should return empty string for None input"
        
        # Test with empty string
        result = html_file.dumps("")
        assert result == "", "Should return empty string for empty input"
    
    def test_html_file_dumps_various_types(self, tmp_path) -> None:
        """Test HtmlFile dumps method with various input types."""
        self._setup_with_tmp_path(tmp_path)
        
        html_file = self._create_html_file("sample.html", tmp_path)
        
        # Test with different types that should be converted to string
        # Note: False becomes "" due to "content or ''" logic in HtmlFile.dumps()
        test_cases = [
            (123, "123"),
            (True, "True"),
            (False, ""),  # False is falsy, so becomes empty string
            ([1, 2, 3], "[1, 2, 3]"),
            ({"key": "value"}, str({"key": "value"})),  # Dict representation may vary
        ]
        
        for input_val, expected in test_cases:
            result = html_file.dumps(input_val)
            assert result == expected, f"Should convert {type(input_val)} to string correctly"
            assert isinstance(result, str), "Result should always be string"
    
    def test_html_file_with_unicode(self, tmp_path) -> None:
        """Test HtmlFile handles Unicode content correctly."""
        self._setup_with_tmp_path(tmp_path)
        
        html_file = self._create_html_file("sample.html", tmp_path)
        
        # Test with Unicode HTML content
        unicode_html = """
        <html>
            <head><title>Tëst Pàgé 🚀</title></head>
            <body>
                <h1>Wëlcömé tö Ünïcödé 🎉</h1>
                <p>Émöjïs: 🔥✨🌟</p>
            </body>
        </html>
        """
        
        # Load and dump Unicode content
        loaded = html_file.loads(unicode_html)
        dumped = html_file.dumps(loaded)
        
        # Should preserve Unicode characters
        assert loaded == unicode_html, "Should preserve Unicode in loads"
        assert dumped == unicode_html, "Should preserve Unicode in dumps"
        assert "🚀" in dumped, "Should preserve emoji characters"
        assert "Ünïcödé" in dumped, "Should preserve accented characters"
