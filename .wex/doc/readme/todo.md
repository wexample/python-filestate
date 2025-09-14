# TODO: Filestate Architecture Improvements

## 1. ✅ Invert Operation-Option Relationship

**Current Issue**: Operations currently check for the presence of options that could trigger them. This creates tight coupling and makes the system harder to maintain.

**Example**: In `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/PIP/pip/filestate/src/wexample_filestate/operation/file_write_operation.py`, the operation checks for multiple scenarios that could trigger it.

**Proposed Solution**: 
- Move the logic from operations to options
- Options should define which operations to execute
- This inverts the dependency: options → operations (instead of operations → options)
- Each option becomes responsible for determining when its associated operation should run

**Benefits**:
- Cleaner separation of concerns
- Options become the single source of truth for when operations should execute
- Easier to maintain and extend

**Status**: ✅ **COMPLETED** - Options now define required operations via `get_required_operations()`

## 2. ✅ Remove Operation Dependencies System

**Current Issue**: Operations have dependencies on each other (e.g., GitCreateBranchOperation depends on GitInitOperation), creating complex dependency resolution.

**Proposed Solution**:
- Remove the entire dependency mechanism between operations
- Execute only one operation per script run
- Re-run the script multiple times until no more operations are needed
- Each execution cycle applies a single operation without considering previous or subsequent operations

**Benefits**:
- Simplified execution model
- No complex dependency resolution needed
- More predictable behavior
- Easier debugging and testing
- Iterative approach ensures eventual consistency

**Implementation Notes**:
- Script should exit after applying one operation
- User runs script repeatedly until system reaches desired state
- Each run evaluates current state independently

**Status**: ✅ **COMPLETED** - Eliminated `applicable()` methods and `dependencies()` system

## Implementation Summary

### What Has Been Accomplished:

1. **Inverted option-operation relationship**: Options now define required operations via `get_required_operations()`
2. **Removed operation dependencies**: Eliminated `applicable()` methods and `dependencies()` system  
3. **Single-operation execution**: Modified `AbstractItemTarget` to find and execute only one operation per run

### Key Changes Made:

- **AbstractItemConfigOption**: Created intermediate class with `get_required_operations()` and `is_satisfied()` methods
- **AbstractOperation**: Removed `applicable()`, `applicable_for_option()`, and `dependencies()` methods
- **AbstractItemTarget**: Added `find_next_operation()` method that iterates through options to find first unsatisfied one

### Next Steps:
- Test the new resolution system
- Update individual options to implement the new methods
- Update individual operations to work with the new system