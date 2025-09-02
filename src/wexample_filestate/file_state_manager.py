from __future__ import annotations

import importlib
import pkgutil
import sys

from wexample_config.const.types import DictConfig
from wexample_filestate.item.item_target_directory import ItemTargetDirectory
from pydantic import BaseModel


class FileStateManager(ItemTargetDirectory):
    def __init__(self, **data) -> None:
        super().__init__(value=None, **data)

    def configure(self, config: DictConfig) -> None:
        super().configure(config=config)

        # As root
        self.build_item_tree()

    @staticmethod
    def load_imports() -> None:
        """Eagerly import filestate submodules and rebuild Pydantic models.

        This avoids Pydantic v2 'class-not-fully-defined' issues due to
        circular or late imports by ensuring all relevant modules are loaded
        before model_rebuild is invoked.
        """
        # 1) Import foundational packages first
        loaded_packages = (
            # filestate core packages
            "wexample_filestate.const",
            "wexample_filestate.result",
            "wexample_filestate.operation",
        )
        for pkg_name in loaded_packages:
            try:
                pkg = importlib.import_module(pkg_name)
            except Exception:
                continue
            if hasattr(pkg, "__path__"):
                for mod in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
                    try:
                        importlib.import_module(mod.name)
                    except Exception:
                        # Best effort: some optional modules may fail to import
                        pass

        # 2) Build a parent namespace with symbols from the loaded packages to resolve bare names
        parent_ns: dict[str, object] = {}
        for name, module in list(sys.modules.items()):
            if not module:
                continue
            if any(name == pkg or name.startswith(pkg + ".") for pkg in loaded_packages):
                try:
                    parent_ns.update(vars(module))
                except Exception:
                    pass

        # 3) Rebuild all Pydantic models (two passes for forward refs)
        seen: set[type] = set()
        stack = list(BaseModel.__subclasses__())
        while stack:
            cls = stack.pop()
            if cls in seen:
                continue
            seen.add(cls)
            # Provide a broad namespace for forward ref resolution
            try:
                setattr(cls, "__pydantic_parent_namespace__", parent_ns)
            except Exception:
                pass
            try:
                cls.model_rebuild()
            except Exception:
                # Ignore, next pass may resolve
                pass
            stack.extend(cls.__subclasses__())

        for cls in list(seen):
            try:
                setattr(cls, "__pydantic_parent_namespace__", parent_ns)
                cls.model_rebuild()
            except Exception:
                pass

