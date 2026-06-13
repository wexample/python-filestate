# Replace str(type(e)) substring checks with set membership on __name__

**Source**: `packages/filestate/src/wexample_filestate/testing/abstract_structured_file_test.py:81`
**Agent**: agent:performance
**Bucket**: set-membership
**Severity**: perf

## Symptom
`"ConvertError" in str(type(e)) or "ValueError" in str(type(e))` builds two strings and performs O(n) substring searches instead of a direct O(1) name lookup.

## Suggested direction
Replace with `type(e).__name__ in {"ConvertError", "ValueError"}` — but verify whether the original substring match was intentional to cover subclass names containing those strings (e.g. `NotConvertError`), and align accordingly.
