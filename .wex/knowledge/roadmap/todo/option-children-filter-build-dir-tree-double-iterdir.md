# `_build_dir_tree` iterates the same directory twice via two sequential `iterdir()` calls

**Source**: `packages/filestate/src/wexample_filestate/option/children_filter_option.py:110-138`
**Agent**: agent:performance
**Bucket**: restructure
**Severity**: perf

## Symptom
`_build_dir_tree` calls `base_dir.iterdir()` twice in sequence — once to collect matching files (lines 110-116) and once to recurse into subdirectories (lines 119-138). Each call issues a separate OS directory-listing syscall, doubling I/O cost for every level of recursion.

## Suggested direction
Collapse the two loops into a single `iterdir()` pass, dispatching on `entry.is_file()` / `entry.is_dir()` inside the loop body; validate that the current children ordering (files before dirs) is not semantically required before merging.
