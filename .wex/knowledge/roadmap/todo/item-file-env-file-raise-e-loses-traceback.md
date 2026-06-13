# `loads` re-raises with `raise e` instead of bare `raise`

**Source**: `packages/filestate/src/wexample_filestate/item/file/env_file.py:37`
**Agent**: agent:performance
**Bucket**: inconsistency
**Severity**: inconsistency

## Symptom
`raise e` replaces the original traceback with a new one starting at that line, making exception origins harder to debug.

## Suggested direction
Replace `raise e` with bare `raise` to preserve the original exception traceback.
