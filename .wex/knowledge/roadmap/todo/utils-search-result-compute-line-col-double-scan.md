# _compute_line_col scans the content prefix twice

**Source**: `packages/filestate/src/wexample_filestate/utils/search_result.py:109`
**Agent**: agent:performance
**Bucket**: benchmark-first
**Severity**: perf

## Symptom
`_compute_line_col` calls `content.count("\n", 0, idx)` and `content.rfind("\n", 0, idx)` sequentially, each scanning the same O(idx) prefix; this doubles the scan cost on every match, which compounds when `create_for_all_matches` finds many results in a large file.

## Suggested direction
Profile against a large file with many matches; if hot, replace both calls with a single manual scan that computes both `line` and `last_newline_pos` in one pass.
