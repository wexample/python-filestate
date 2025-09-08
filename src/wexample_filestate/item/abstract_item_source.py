from __future__ import annotations

import attrs
from wexample_helpers.classes.base_class import BaseClass


@attrs.define(kw_only=True)
class AbstractItemSource(BaseClass):
    pass
