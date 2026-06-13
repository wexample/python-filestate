# Mutable class-level default _executed_operations shared across instances

**Source**: `packages/filestate/src/wexample_filestate/result/file_state_result.py:12`
**Agent**: agent:performance
**Bucket**: restructure
**Severity**: bug

## Symptom
`_executed_operations: list = []` is declared at class level, so all instances share the
same list object. Any append/mutation on one instance silently contaminates others.

## Suggested direction
Move the initialisation to `__init__` (or a Pydantic `Field(default_factory=list)` if
the class is a Pydantic model) so each instance gets its own list.
