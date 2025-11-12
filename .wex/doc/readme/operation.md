# Operations

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

## Operation Execution Model

### Single Operation Per Pass
Each option can only return **one operation per execution pass**. This means complex scenarios require multiple passes:

**Example**: File doesn't exist + needs specific content + wrong permissions
- **Pass 1**: `ShouldExistOption` creates `FileWriteOperation` (creates empty file)
- **Pass 2**: `ContentOption` creates `FileWriteOperation` (adds content)  
- **Pass 3**: `ModeOption` creates `ItemChangeModeOperation` (sets permissions)

This sequential approach ensures:
- Each operation has a clear, single responsibility
- Operations can depend on previous operations being completed
- The system remains predictable and debuggable

### Conditional Operations
Options only create operations when changes are actually needed:
- File already has correct content → No operation
- File doesn't exist but should → Create `FileWriteOperation`
- File has wrong permissions → Create `ItemChangeModeOperation`

This design ensures efficiency and idempotency - running the same configuration multiple times produces the same result without unnecessary work.

## Operation Simplification

### Generic Operations
Options create generic operations (`FileWriteOperation`, `ItemChangeModeOperation`) instead of specialized ones, making the system more maintainable.

**Before**: Many specialized operations like `ContentLinesSortOperation`, `ContentLinesUniqueOperation`, `ContentTrimOperation`
**After**: Single generic `FileWriteOperation` with options handling the logic

### Operation Lifecycle
1. **Creation**: Option analyzes state and creates operation if needed
2. **Validation**: Operation validates it can be executed
3. **Execution**: Operation performs the actual filesystem changes
4. **Rollback**: Operation can undo changes if needed
