# XmlFile.loads uses `raise e` which resets exception traceback

**Source**: `packages/filestate/src/wexample_filestate/item/file/xml_file.py:32`
**Agent**: agent:performance
**Bucket**: restructure
**Severity**: bug

## Symptom
`raise e` inside the `except` block re-raises the exception but resets the traceback
origin to that line, hiding the real parse error location from callers.

## Suggested direction
Replace `raise e` with a bare `raise` to preserve the original traceback.
