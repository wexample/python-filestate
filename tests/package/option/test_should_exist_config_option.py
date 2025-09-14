from __future__ import annotations

from typing import Any

from wexample_filestate.testing.test_abstract_operation import TestAbstractOperation


class TestShouldExistConfigOption(TestAbstractOperation):
    def _operation_get_count(self) -> int:
        return 0

    def _operation_test_setup_configuration(self) -> Any | None:
        from wexample_filestate.option.should_exist_option import (
            ShouldExistOption,
        )

        return {
            # Simply test this configuration format.
            ShouldExistOption
        }
