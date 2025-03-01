# Filestate

Package that allows you to manage the state of files and directories using YAML configuration files.

Version: 0.0.30

## Features

- **Apply and Modify Permissions and Ownership**: Manage file and directory permissions and ownership individually or recursively.
- **Create, Modify, and Delete Directories**: Use patterns and regex to create, modify, and delete directories and subdirectories (e.g., ensure each `Entity/MyEntity.php` file has a corresponding `Repository/MyEntityRepository.php`).
- **Create Files Using Templates and Placeholders**: Generate files from templates with dynamic placeholders.


## Requirements

- Python >=3.6

## Dependencies

- pip-tools
- pydantic
- pytest
- wexample-config==0.0.30
- wexample-helpers==0.0.30
- wexample-prompt==0.0.31

## Installation

```bash
pip install wexample-filestate
```

## Usage


### Configuration File Example

```yaml
# example.yaml
children:
  - path: /path/to/file
    owner: user
    group: group
    mode: '0644'
  - path: /path/to/directory
    recursive: true
    mode: '0755'
    create: true
```

## Usage

Here's how you can use filestate in your Python code:

```
from filestate import FileStateManager

# Initialize the state manager with the root directory
state_manager = FileStateManager('root/directory/')

# Configure the state manager from a YAML configuration file
state_manager.configure_from_file('configuration.yaml')

# Perform a dry run to see what changes would be made
result = state_manager.dry_run()
result.print()

# Check if the configuration can be successfully applied
if state_manager.succeed():
    # Apply the configuration
    state_manager.apply()
else:
    print("Configuration could not be applied successfully.")

```

### Applying and Modifying Permissions

```
state_manager = FileStateManager('/var/www/')
state_manager.configure({
    'files': [
        {'path': '/var/www/index.html', 'owner': 'www-data', 'group': 'www-data', 'mode': '0644'},
        {'path': '/var/www/css/', 'recursive': True, 'owner': 'www-data', 'group': 'www-data', 'mode': '0755'}
    ]
})
state_manager.apply()
```

### Applying and Modifying Permissions

```
state_manager = FileStateManager('/project/')
state_manager.configure({
    'directories': [
        {'path': '/project/src/Entity/', 'create': True},
        {'path': '/project/src/Repository/', 'create': True, 'pattern': 'Entity/*Entity.php', 'target': 'Repository/*Repository.php'}
    ]
})
state_manager.apply()
```

## Links

- Homepage: https://github.com/wexample/python-filestate

## License

MIT
## Credits

This package has been developed by [Wexample](https://wexample.com), a collection of tools and utilities to streamline development workflows.

Visit [wexample.com](https://wexample.com) to discover more tools and resources for efficient development.