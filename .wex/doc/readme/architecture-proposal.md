# New Architecture Proposal: Option-Driven Operations

## Core Principle

Options create and configure operation instances when their requirements are not satisfied. This inverts the current relationship where operations check for applicable options.

## Key Changes

### 1. Option Responsibility Expansion

**New OptionMixin Methods:**
```python
@abstract_method
def is_satisfied(self, target) -> bool:
    """Check if the current state satisfies this option's requirements."""
    pass

@abstract_method  
def create_required_operation(self, target) -> AbstractOperation | None:
    """Create and configure an operation instance when this option is not satisfied.
    
    Returns None if no operation is needed.
    The option is responsible for:
    - Instantiating the appropriate operation class
    - Configuring the operation with necessary data
    - Passing any computed values (e.g., new content for FileWriteOperation)
    """
    pass
```

### 2. Simplified Operation Interface

**Removed from AbstractOperation:**
- `applicable()` method
- `applicable_for_option()` method  
- `dependencies()` method

**Operations become pure executors:**
- Receive pre-configured data from options
- Focus solely on applying changes
- No longer responsible for determining applicability

### 3. New Resolution Logic

**Modified AbstractItemTarget.build_operations():**
```python
def build_operations(self, result: AbstractResult, ...) -> bool:
    # Iterate through options instead of operations
    for option in self.options.values():
        if not option.is_satisfied(self.target):
            operation = option.create_required_operation(self.target)
            if operation:
                result.operations.append(operation)
                # Execute only ONE operation per run
                return True
    return False
```

### 4. Single Operation Execution

Each script execution:
1. Evaluates all options
2. Finds the first unsatisfied option
3. Creates and executes its required operation
4. Exits (user re-runs script for next operation)

## Example Implementation

### ContentOption (creates FileWriteOperation with specific content)

```python
class ContentOption(OptionMixin):
    def is_satisfied(self, target) -> bool:
        current_content = target.get_current_content()
        expected_content = self.get_value().get_str()
        return current_content == expected_content
    
    def create_required_operation(self, target) -> AbstractOperation | None:
        if self.is_satisfied(target):
            return None
            
        expected_content = self.get_value().get_str()
        operation = FileWriteOperation(target=target)
        operation.set_new_content(expected_content)  # Option provides the content
        return operation
```

### ShouldContainLinesOption (creates FileWriteOperation with appended lines)

```python
class ShouldContainLinesOption(OptionMixin):
    def is_satisfied(self, target) -> bool:
        current_lines = target.get_current_content().splitlines()
        required_lines = self.get_value().get_list()
        return all(line in current_lines for line in required_lines)
    
    def create_required_operation(self, target) -> AbstractOperation | None:
        if self.is_satisfied(target):
            return None
            
        current_content = target.get_current_content()
        required_lines = self.get_value().get_list()
        
        # Option computes the new content
        new_content = self._append_missing_lines(current_content, required_lines)
        
        operation = FileWriteOperation(target=target)
        operation.set_new_content(new_content)
        return operation
```

## Benefits

1. **Clear Separation**: Options handle logic, operations handle execution
2. **Data Flow**: Options compute and provide data to operations
3. **Simplicity**: No complex dependency resolution
4. **Predictability**: Deterministic single-operation execution
5. **Extensibility**: Easy to add new option/operation pairs
