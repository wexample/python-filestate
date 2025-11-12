# Options

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

### Legacy Compatibility
Many options support both simple and nested formats:
```yaml
# Simple format (legacy)
"content": "just text"

# Nested format (extended)
"content": {
    "text": "just text",
    "sort_lines": false
}
```

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

### Logic Consolidation
Modern options consolidate logic that was previously scattered across multiple operations:

**Before**: Separate `ContentLinesSortOperation` and `ContentLinesUniqueOperation`
**After**: Single `ContentOption` with integrated sorting and deduplication logic

### Common Patterns

#### Validation and Enforcement
Some options work in pairs to validate and enforce rules:

```yaml
"name_format": {
    "case_format": "lowercase"
}
"on_bad_format": {
    "action": "rename"  # or "delete", "ignore", "error"
}
```
