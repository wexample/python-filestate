import os.path

from wexample_filestate.const.types_state_items import TargetFileOrDirectory
from wexample_filestate.options_values.content_option_value import ContentOptionValue
from wexample_helpers.helpers.directory_helper import directory_aggregate_all_files


class TemplatesAggregationContentOptionValue(ContentOptionValue):
    templates_dir_path: str

    def render(self, target: TargetFileOrDirectory, current_value: str) -> str:
        return directory_aggregate_all_files(os.path.join(target.path.parent, self.templates_dir_path))
