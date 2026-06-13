# truthy-check on templates blocked by None type annotation

**Source**: `packages/filestate/src/wexample_filestate/config_value/aggregated_templates_config_value.py:37`
**Agent**: agent:performance
**Bucket**: truthy-check
**Severity**: typing

## Symptom
`if len(templates) == 0:` could be replaced with `if not templates:`, but `templates` is typed `list[str] | None`, so `not None` is True while `len(None)` raises TypeError — semantics differ when the value is None.

## Suggested direction
Narrow the return type of `get_templates()` to `list[str]` (since the field uses `factory=list` and is never explicitly set to None) and then apply the truthy-check safely.
