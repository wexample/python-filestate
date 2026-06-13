# read_parsed staleness does not clear _content_cache_config

**Source**: `packages/filestate/src/wexample_filestate/item/file/structured_content_file.py:108`
**Agent**: agent:performance
**Bucket**: benchmark-first
**Severity**: bug

## Symptom
When `read_parsed(reload=False)` is called and `_is_cache_stale()` returns True, the parsed cache is refreshed from disk but `_content_cache_config` is left pointing at the old data. A subsequent `read_config()` call may return a stale `NestedConfigValue` without re-reading the freshly parsed content.

## Suggested direction
Inside the `if reload or self._parsed_cache is None or self._is_cache_stale():` branch, also clear `_content_cache_config` unconditionally (not only when `reload` is True), mirroring what `_on_disk_reload` already does.
