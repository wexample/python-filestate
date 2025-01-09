# Project Conventions

You are reading this file to understand the basic conventions of the project.

## Concepts

### Config Option

A `Config Option` defines a `key` that the user can set in the configuration file or class to specify a file or directory property. For example, the `should_exist` key determines whether a file or directory should exist. If set to `true`, the file or directory will always be created; if set to `false`, it will always be deleted.

An option can take simple values, such as strings, booleans, integers, etc., or use classes defined in the `config_value` directory.

### Config Option Provider

A `Config Option Provider` allows options to be grouped, as certain options may not be relevant for all projects (e.g., depending on the language, framework, etc.).

### Config Value

`Config Value` classes allow dynamic configuration values to be generated based on the context. For example, they can use templates to generate file content dynamically.

### Operation

An `Operation` defines the actions to be executed when a related config option is set. For instance, creating or removing a file when the `should_exist` config option is configured.

### Operations Provider

An `Operations Provider` allows operations to be grouped, as certain operations may not be relevant for all projects (e.g., depending on the language, framework, etc.).
