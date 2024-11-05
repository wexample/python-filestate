from typing import Type, Any, Union

from wexample_filestate.item.item_target_directory import ItemTargetDirectory
from wexample_helpers.helpers.import_helper import import_dummy
from wexample_helpers.test.abstract_test_helpers import AbstractTestHelpers


class TestFileStateManager(AbstractTestHelpers):
    def test_types(self):
        from wexample_filestate.file_state_manager import FileStateManager
        from wexample_filestate.config_option.child_factory_config_option import ChildFactoryConfigOption
        from wexample_filestate.result.abstract_result import AbstractResult

        import_dummy(AbstractResult)

        class TestClass(FileStateManager):
            pass

        self._test_type_validate_or_fail(
            success_cases=[
                (TestClass, Type[ItemTargetDirectory]),
                ([ChildFactoryConfigOption(pattern={})], list[ChildFactoryConfigOption]),
                ([ChildFactoryConfigOption(pattern={})], list[Union[dict[str, Any], ChildFactoryConfigOption]])
            ]
        )
