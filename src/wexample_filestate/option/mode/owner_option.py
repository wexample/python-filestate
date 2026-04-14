from __future__ import annotations

from typing import Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.enum.scopes import Scope
from wexample_filestate.option.mixin.option_mixin import OptionMixin


@base_class
class OwnerOption(OptionMixin, AbstractConfigOption):
    @classmethod
    def get_scopes(cls) -> list[Scope]:
        return [Scope.OWNERSHIP]

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return str

    @staticmethod
    def resolve(raw: str) -> tuple[int | None, int | None]:
        """Resolve an owner string to a (uid, gid) tuple.

        Accepted formats:
          "999:999"         -> (999, 999)
          "mongodb:mongodb" -> (resolved uid, resolved gid)
          "999"             -> (999, None)  -- gid unchanged
          "999:"            -> (999, None)
          ":999"            -> (None, 999)  -- uid unchanged
        """
        import grp
        import pwd

        parts = raw.split(":", 1)
        user_part = parts[0].strip() if parts[0].strip() else None
        group_part = parts[1].strip() if len(parts) > 1 and parts[1].strip() else None

        uid: int | None = None
        if user_part is not None:
            try:
                uid = int(user_part)
            except ValueError:
                uid = pwd.getpwnam(user_part).pw_uid

        gid: int | None = None
        if group_part is not None:
            try:
                gid = int(group_part)
            except ValueError:
                gid = grp.getgrnam(group_part).gr_gid

        return uid, gid

    def get_description(self) -> str:
        return (
            "File owner in 'uid:gid', 'user:group', or 'uid' format. "
            "Both numeric IDs and symbolic names are accepted."
        )
