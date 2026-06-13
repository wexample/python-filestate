# read_bytes computes _is_cache_stale() before short-circuiting on reload=True

**Source**: `packages/filestate/src/wexample_filestate/item/mixins/item_file_mixin.py:77`
**Agent**: agent:performance
**Bucket**: benchmark-first
**Severity**: perf

## Symptom
`stale = self._is_cache_stale()` triggers a `stat()` syscall unconditionally on every
`read_bytes` call, even when `reload=True` (where the result of `stale` is irrelevant
to the branching because `reload` already forces entry into the block).

## Suggested direction
Defer the stale check with `stale = not reload and self._bytes_cache is not None and
self._is_cache_stale()` so the stat is skipped when `reload=True`. Verify the edge
case where `_bytes_cache is None` but `_cache_mtime_ns is not None` (file read returned
None) to confirm `_on_disk_reload()` call semantics are preserved before applying.
