# apply_operations: use set for _executed_operations membership check

**Source**: `packages/filestate/src/wexample_filestate/result/abstract_result.py:39`
**Agent**: agent:performance
**Bucket**: set-membership
**Severity**: perf

## Symptom
`self._executed_operations` is initialised as a list and checked with `if operation in self._executed_operations` on every loop iteration, giving O(n) membership cost per operation.

## Suggested direction
Change `self._executed_operations = []` to a `set()` and replace `.append()` with `.add()`; verify first that `AbstractOperation` (and all subclasses) do not define `__eq__` without a matching `__hash__`, otherwise the objects will be unhashable and the swap will raise at runtime.
