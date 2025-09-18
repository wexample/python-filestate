# Migration Protocol: Option/Operation Conversion

## For Each Option

1. **Inherit from AbstractItemConfigOption** instead of AbstractConfigOption
2. **Implement create_required_operation(target)** - Return operation instance with parameters or None if satisfied
3. **Remove any operation-checking logic** - Options should not reference operations directly

## For Each Operation

1. **Remove applicable() and applicable_for_option() methods** - No longer needed
2. **Remove dependencies() method** - No longer needed
3. **Keep apply(), undo(), describe_*() methods** - Core functionality remains
4. **Add constructor parameters** - Accept values from options (content, lines, etc.)
5. **Update operation logic** - Use passed parameters instead of querying options
6. **Remove all option lookups** - Operations should be self-contained with data from constructor

## Testing Protocol

After migrating an option/operation pair:

1. **Run existing tests** - Verify migration doesn't break functionality:
   ```bash
   .wex/python/venv/bin/pytest -x tests/package/operation/test_[operation_name].py
   ```

2. **Fix test failures** - Update tests to work with new constructor signatures

3. **Verify integration** - Run broader test suite to ensure no regressions:
   ```bash
   .wex/python/venv/bin/pytest -x tests/package/operation/
   ```

4. **Update test documentation** - Ensure test cases reflect new architecture

## Note

- When moving script from operation to option, if other options script remains in the operation script, comment it, we will remove it when movieng the future option
- Si, if you find commmented option script in operation file, migrate it if it matches with the option you are migrating 

## Options to Migrate

### Core Filestate Options
- [x] active_config_option.py
- [ ] children_config_option.py
- [ ] children_file_factory_config_option.py``
- [ ] children_filter_config_option.py
- [ ] class_config_option.py
- [ ] content_config_option.py
- [ ] content_options_config_option.py
- [ ] default_content_config_option.py
- [x] mode_config_option.py
- [ ] mode_recursive_config_option.py
- [x] name_pattern_config_option.py
- [ ] remove_backup_max_file_size_config_option.py
- [ ] shortcut_config_option.py
- [ ] should_contain_lines_config_option.py
- [ ] should_exist_config_option.py
- [ ] should_have_extension_config_option.py
- [ ] should_not_contain_lines_config_option.py
- [ ] text_filter_config_option.py
- [ ] type_config_option.py
- [ ] yaml_filter_config_option.py

### Git Options
- [ ] create_remote_config_option.py
- [ ] git_config_option.py
- [ ] main_branch_config_option.py
- [ ] remote_config_option.py
- [ ] remote_item_config_option.py
- [ ] type_config_option.py (git)

### Python Options
- [ ] python_config_option.py

## Operations to Migrate

### Core Filestate Operations
- [ ] content_ensure_newline_operation.py
- [ ] content_lines_sort_operation.py
- [ ] content_lines_unique_operation.py
- [ ] content_trim_operation.py
- [ ] file_change_extension_operation.py
- [ ] file_create_operation.py
- [ ] file_remove_operation.py
- [ ] file_write_operation.py
- [x] item_change_mode_operation.py
- [ ] yaml_sort_recursive_operation.py

### Git Operations
- [ ] git_create_branch_operation.py
- [ ] git_init_operation.py
- [ ] git_remote_add_operation.py
- [ ] git_remote_create_operation.py

### Python Operations
- [ ] python_add_future_annotations_operation.py
- [ ] python_add_return_types_operation.py
- [ ] python_fix_attrs_operation.py
- [ ] python_fix_blank_lines_operation.py
- [ ] python_format_operation.py
- [ ] python_fstringify_operation.py
- [ ] python_modernize_typing_operation.py
- [ ] python_order_class_attributes_operation.py
- [ ] python_order_class_docstring_operation.py
- [ ] python_order_class_methods_operation.py
- [ ] python_order_constants_operation.py
- [ ] python_order_iterable_items_operation.py
- [ ] python_order_main_guard_operation.py
- [ ] python_order_module_docstring_operation.py
- [ ] python_order_module_functions_operation.py
- [ ] python_order_module_metadata_operation.py
- [ ] python_order_type_checking_block_operation.py
- [ ] python_relocate_imports_operation.py

