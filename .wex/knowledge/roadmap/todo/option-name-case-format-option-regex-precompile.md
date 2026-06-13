# Pre-compile regex patterns to class-level constants

**Source**: `packages/filestate/src/wexample_filestate/option/name/case_format_option.py:35`
**Agent**: agent:performance
**Bucket**: restructure
**Severity**: perf

## Symptom
Four regex patterns (two in `apply_correction` for snake_case/kebab-case, three in `_is_camel_case`/`_is_snake_case`/`_is_kebab_case`) are recompiled on every call. `re.sub`/`re.match` with string literals skip the compile cache under high call frequency.

## Suggested direction
Lift the six patterns to class-level `re.compile(...)` attributes and reference those compiled objects inside the methods; this is a class-level change that falls outside single-method scope.
