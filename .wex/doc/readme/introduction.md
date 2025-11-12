# Introduction to Filestate

Filestate is a file management system that ensures files and directories conform to specified standards through automated operations and configuration options.

## Core Concepts

### Items
Each "item" represents a file or directory in the system. Items exist in two states:
- **Source items**: Files or directories as they currently exist
- **Target items**: Files or directories as they should exist according to the defined standards

### Options and Operations
The system operates through a provider-based architecture:

**Options**: Define the desired properties and standards that files should meet (e.g., "files must end with a newline character")

**Operations**: Execute the necessary transformations to achieve the desired state (e.g., "add a newline at the end of the file")

### Processing Logic
When an item already meets the required standards, the source and target remain identical - no operation is needed. However, when an option defines a property that is not currently effective, the corresponding operation is executed to transform the source item into the target state.

This approach ensures that your codebase maintains consistency and adheres to your defined standards automatically, reducing manual maintenance overhead and improving code quality.

## Configuration Examples

### File Removal
Specify that a file should not exist - if found, it will be removed by the FileRemoveOperation:

```json
{
    "name": "requirements.in",
    "type": "DiskItemType.FILE",
    "should_exist": false
}
```

### Content Requirements
Ensure a file contains specific lines - missing content will be added automatically:

```json
{
    "name": ".gitignore",
    "type": "DiskItemType.FILE", 
    "should_exist": true,
    "should_contain_lines": ["ignore-this.txt"]
}
```

These examples demonstrate how filestate configurations define both structural requirements (file existence) and content requirements (specific lines or patterns).