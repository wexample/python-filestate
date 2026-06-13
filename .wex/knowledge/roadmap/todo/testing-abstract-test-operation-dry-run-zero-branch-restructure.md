# _operation_test_dry_run duplicates _dry_run_and_count_operations for zero-count case

**Source**: `packages/filestate/src/wexample_filestate/testing/abstract_test_operation.py:59`
**Agent**: agent:performance
**Bucket**: restructure
**Severity**: style

## Symptom
The `expected_count == 0` branch in `_operation_test_dry_run` (lines 65–69) repeats the
exact logic of `_dry_run_and_count_operations`; the only difference is a slightly different
assertion message string ("operations" vs "operation(s)").

## Suggested direction
Remove the conditional branch and let `_dry_run_and_count_operations` handle all cases
uniformly, since it already calls `_operation_get_count()` and asserts equality against it.
