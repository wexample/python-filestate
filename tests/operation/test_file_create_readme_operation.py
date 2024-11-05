import os
from typing import Optional

from wexample_config.const.types import DictConfig
from wexample_filestate.config_value.readme_content_option_value import ReadmeContentConfigValue
from wexample_filestate.test.test_abstract_operation import TestAbstractOperation


class TestFileCreateReadmeOperation(TestAbstractOperation):
    missing_file_name: str = 'simple-readme.md'

    def _operation_test_setup_configuration(self) -> Optional[DictConfig]:
        from wexample_filestate.const.disk import DiskItemType

        return {
            'children': [
                {
                    'name': self.missing_file_name,
                    'should_exist': True,
                    'type': DiskItemType.FILE,
                    'default_content': ReadmeContentConfigValue(
                        templates=[
                            '## Introduction',
                            '## License'
                        ],
                        parameters={}
                    )
                }
            ]
        }

    def _operation_get_count(self) -> int:
        return 1

    def _operation_test_assert_initial(self) -> None:
        target_file = self.state_manager.find_by_name_or_fail(self.missing_file_name)

        assert not os.path.exists(target_file.get_resolved()), "The file should not exist"

    def _operation_test_assert_applied(self):
        target_file = self.state_manager.find_by_name_or_fail(self.missing_file_name)

        assert os.path.exists(target_file.get_resolved()), "The target file should have been created"
