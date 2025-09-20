# Options and Operations

## What are Options?

Options are configuration properties that define the desired state of files and directories. When you write a filestate configuration, you're primarily working with options:

```yaml
{
    "name": "my_file.txt",
    "should_exist": true,
    "type": "file",
    "content": "Hello World",
    "mode": "644",
    "text": {
        "trim": true,
        "end_new_line": true
    }
}
```

Each key in your configuration corresponds to an option class:
- `name` → `NameOption`
- `should_exist` → `ShouldExistOption`
- `content` → `ContentOption`
- `mode` → `ModeOption`
- `text` → `TextOption`

## Option Types

### Simple Options
Accept a single value:
```yaml
"name": "file.txt"
"should_exist": true
"mode": "755"
```

### Nested Options
Accept structured configuration with multiple sub-options:
```yaml
"content": {
    "text": "file content",
    "sort_lines": true,
    "unique_lines": true
}

"name_format": {
    "case_format": "lowercase",
    "prefix": "test_",
    "regex": "^test_.*\\.txt$"
}
```

## How Options Create Operations

Options don't just store configuration - they actively analyze the current state and create operations when changes are needed.

### The Process

1. **State Analysis**: Each option compares the desired state (configuration) with the current state (filesystem)

2. **Operation Creation**: If changes are needed, the option creates an appropriate operation via `create_required_operation()`

3. **Operation Execution**: The system executes all created operations to reach the desired state

### Example Flow

```yaml
"content": {
    "text": "line3\nline1\nline2",
    "sort_lines": true
}
```

1. `ContentOption` reads current file content: `"line3\nline1\nline2"`
2. Applies sorting logic: `"line1\nline2\nline3"`
3. Compares with current content - they differ
4. Creates `FileWriteOperation` with sorted content
5. Operation executes, writing the sorted content to file

## Option Architecture

### Configuration Processing
Options handle multiple input formats and convert them to a standardized internal representation:

```python
# String input
raw_value = "my_file.txt"

# Converted internally to
raw_value = {
    "value": "my_file.txt"
}
```

### Conditional Operations
Options only create operations when changes are actually needed:
- File already has correct content → No operation
- File doesn't exist but should → Create `FileWriteOperation`
- File has wrong permissions → Create `ItemChangeModeOperation`

This design ensures efficiency and idempotency - running the same configuration multiple times produces the same result without unnecessary work.