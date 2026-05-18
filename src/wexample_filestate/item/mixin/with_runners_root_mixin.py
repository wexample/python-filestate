from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_runner.runner.docker_runner import DockerRunner


@base_class
class WithRunnersRootMixin:
    _batch_content_cache: dict[str, dict[str, str]] = public_field(
        factory=dict,
        description="Per-option batch content caches: {option_name: {path: new_content}}.",
    )
    _rectify_hash_cache: dict[str, str] = public_field(
        factory=dict,
        description="MD5 hashes of files after last rectification, keyed by path.",
    )
    _runner_cache: dict[str, DockerRunner] = public_field(
        factory=dict, description="Docker runners cache keyed by image name."
    )

    def get_batch_cache(self, key: str) -> dict[str, str] | None:
        return self._batch_content_cache.get(key)

    def get_rectify_hash(self, path: str) -> str | None:
        return self._rectify_hash_cache.get(path)

    def get_runner(self, image_name: str) -> DockerRunner | None:
        return self._runner_cache.get(image_name)

    def set_batch_cache(self, key: str, cache: dict[str, str]) -> None:
        self._batch_content_cache[key] = cache

    def set_rectify_hash(self, path: str, hash: str) -> None:
        self._rectify_hash_cache[path] = hash

    def set_runner(self, image_name: str, runner: DockerRunner | None) -> None:
        if runner is None:
            self._runner_cache.pop(image_name, None)
        else:
            self._runner_cache[image_name] = runner

    def stop_runners(self) -> None:
        """Stop all Docker runners attached to this root."""
        for runner in self._runner_cache.values():
            runner.stop()
        self._runner_cache.clear()
