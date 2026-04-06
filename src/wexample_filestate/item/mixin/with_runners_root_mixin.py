from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_runner.runner.docker_runner import DockerRunner


@base_class
class WithRunnersRootMixin:
    _runner_cache: dict[str, "DockerRunner"] = public_field(
        factory=dict, description="Docker runners cache keyed by image name."
    )

    def get_runner(self, image_name: str) -> "DockerRunner | None":
        return self._runner_cache.get(image_name)

    def set_runner(self, image_name: str, runner: "DockerRunner | None") -> None:
        if runner is None:
            self._runner_cache.pop(image_name, None)
        else:
            self._runner_cache[image_name] = runner

    def stop_runners(self) -> None:
        """Stop all Docker runners attached to this root."""
        for runner in self._runner_cache.values():
            runner.stop()
        self._runner_cache.clear()
