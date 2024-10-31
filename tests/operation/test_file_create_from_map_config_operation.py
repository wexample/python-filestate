import os
from typing import Optional

from wexample_config.const.types import DictConfig
from wexample_filestate.config_option.child_factory_config_option import ChildFactoryConfigOption
from wexample_filestate.const.disk import DiskItemType
from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
from wexample_filestate.test.test_abstract_operation import TestAbstractOperation


class TestFileCreateFromClassOperation(TestAbstractOperation):
    missing_file_name: str = 'simple-readme.md'

    def _operation_test_setup_configuration(self) -> Optional[DictConfig]:
        from typing import Optional
        from wexample_config.const.types import DictConfig

        class TestClass(FileStateItemFileTarget):
            def prepare_value(self, config: Optional[DictConfig] = None) -> DictConfig:
                config.update()

                return config

        return {
            "children": [
                {
                    "name": "collection",
                    "type": DiskItemType.DIRECTORY,
                    "children": [
                        {
                            "name": "one",
                            "type": DiskItemType.DIRECTORY,
                            "children": [
                                ChildFactoryConfigOption(value={
                                    'class': TestClass,
                                    'name_pattern': r"^test-collection-[a-z]+-[a-z]+\.txt$",
                                    'type': DiskItemType.FILE,
                                    'should_exist': False,
                                })
                            ]
                        }
                    ]
                }

            ]
        }

    def _operation_get_count(self) -> int:
        return 3

    def _operation_test_assert_initial(self) -> None:
        target_file = self.state_manager.find_by_name_recursive("test-collection-one-one.txt")

        assert os.path.exists(target_file.get_resolved()), "The file should exist"

    def _operation_test_assert_applied(self):
        target_file = self.state_manager.find_by_name_recursive("test-collection-one-one.txt")

        assert not os.path.exists(
            target_file.get_resolved()), "The target file have been removed because it matches the name pattern"
