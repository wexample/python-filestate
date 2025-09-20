# Option Testing

## Test Structure and Organization

### File Naming and Location

#### Single Test Class
For options with only one test class:
```
tests/package/option/test_option_name.py
```

#### Multiple Test Classes
For options requiring multiple test scenarios, create a dedicated folder:
```
tests/package/option/option_name/
├── test_simple_case.py
├── test_nested_format.py
├── test_legacy_compatibility.py
└── test_edge_cases.py
```

#### Naming Conflicts
If the option name conflicts with a Python module (git, yaml, etc.), prefix with underscore:
```
tests/package/option/_yaml_option/
├── test_sort_recursive.py
├── test_legacy_format.py
└── test_no_operation.py
```

### Test Class Naming
Test classes should be named in PascalCase following the pattern:
```python
class TestOptionNameSpecificScenario(AbstractTestOperation):
    """Test OptionName with specific scenario description."""
```

Examples:
- `TestContentOptionSimple`
- `TestTextOptionTrimOnly` 
- `TestNameFormatOptionCaseFormat`

## Test Implementation Rules

### Base Class Inheritance
All option tests must inherit from `AbstractTestOperation`:

```python
from wexample_filestate.testing.abstract_test_operation import AbstractTestOperation

class TestMyOption(AbstractTestOperation):
    # Test implementation
```

### Single Operation Testing
Each test should validate **exactly one operation**. This requires careful setup of initial conditions:

#### Testing File Creation
```python
class TestContentOptionSimple(AbstractTestOperation):
    def _operation_test_assert_initial(self) -> None:
        # File must NOT exist initially
        file_path = self._get_absolute_path_from_state_manager("test.txt")
        self._assert_file_exists(file_path=file_path, positive=False)
    
    def _operation_get_count(self) -> int:
        return 1  # Expects FileWriteOperation
```

#### Testing File Modification
```python
class TestModeOptionPermissions(AbstractTestOperation):
    def _operation_test_assert_initial(self) -> None:
        # File must exist with wrong permissions
        file_path = self._get_absolute_path_from_state_manager("existing.txt")
        self._assert_file_exists(file_path=file_path, positive=True)
        # Verify current permissions are different from target
    
    def _operation_get_count(self) -> int:
        return 1  # Expects ItemChangeModeOperation
```

### Required Test Methods

#### Operation Count
```python
def _operation_get_count(self) -> int:
    return 1  # Number of operations expected
```

#### Initial State Validation
```python
def _operation_test_assert_initial(self) -> None:
    # Verify the initial state before operation
    # This ensures we're testing the right operation
```

#### Final State Validation
```python
def _operation_test_assert_applied(self) -> None:
    # Verify the final state after operation
    # This confirms the operation worked correctly
```

#### Configuration Setup
```python
def _operation_test_setup_configuration(self) -> DictConfig | None:
    return {
        "children": [
            {
                "name": "test_file.txt",
                "should_exist": True,
                "type": DiskItemType.FILE,
                "content": "test content",
            }
        ]
    }
```

## Test Factorization

### Parent Test Classes
Create reusable parent classes in `src/package_name/testing/` for common test patterns:

```python
# src/wexample_filestate/testing/abstract_content_test.py
class AbstractContentTest(AbstractTestOperation):
    """Base class for content-related option tests."""
    
    test_content: str = "default content"
    
    def _operation_test_assert_applied(self) -> None:
        file_path = self._get_absolute_path_from_state_manager(self.get_test_filename())
        self._assert_file_content_equals(
            file_path=file_path,
            expected_value=self.test_content,
            positive=True,
        )
    
    def get_test_filename(self) -> str:
        """Override in child classes."""
        raise NotImplementedError
```

### Using Parent Classes
```python
from wexample_filestate.testing.abstract_content_test import AbstractContentTest

class TestContentOptionSimple(AbstractContentTest):
    test_content: str = "SIMPLE_CONTENT"
    
    def get_test_filename(self) -> str:
        return "simple.txt"
    
    def _operation_test_setup_configuration(self) -> DictConfig | None:
        # Specific configuration for this test
```

## Common Test Patterns

### Testing Legacy Compatibility
```python
class TestOptionLegacyFormat(AbstractTestOperation):
    """Test option with legacy string format."""
    
    def _operation_test_setup_configuration(self) -> DictConfig | None:
        return {
            "children": [{
                "name": "test.txt",
                "option_name": "simple_string_value"  # Legacy format
            }]
        }

class TestOptionNestedFormat(AbstractTestOperation):
    """Test option with nested dict format."""
    
    def _operation_test_setup_configuration(self) -> DictConfig | None:
        return {
            "children": [{
                "name": "test.txt",
                "option_name": {  # Nested format
                    "sub_option": "value",
                    "another_option": True
                }
            }]
        }
```

### Testing No Operation Cases
```python
class TestOptionNoOperation(AbstractTestOperation):
    """Test option when no operation is needed."""
    
    def _operation_get_count(self) -> int:
        return 0  # No operation expected
    
    def _operation_test_assert_initial(self) -> None:
        # File already in correct state
        file_path = self._get_absolute_path_from_state_manager("correct.txt")
        self._assert_file_exists(file_path=file_path, positive=True)
        self._assert_file_content_equals(
            file_path=file_path,
            expected_value="correct content",
            positive=True,
        )
```

## Best Practices

1. **One Concern Per Test**: Each test class should focus on one specific scenario
2. **Descriptive Names**: Test class names should clearly indicate what they're testing
3. **Proper Setup**: Ensure initial state matches what the operation expects
4. **Clear Assertions**: Use specific assertions that validate the expected behavior
5. **Reuse Common Logic**: Factor out common patterns into parent classes
6. **Test Edge Cases**: Include tests for boundary conditions and error cases
