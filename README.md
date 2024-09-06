# PyLogger

PyLogger is a robust, feature-rich logging utility for Python applications. It provides an easy-to-use interface for logging messages at various levels, with support for both console and file output.

## Features

-   Singleton design ensures consistent logging across your application
-   Supports standard logging levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
-   Custom log levels: SUCCESS, FAILED, MESSAGE
-   Colored console output for better readability
-   File logging for persistent records
-   Exception logging with stack trace
-   Configurable console log level via environment variable
-   JSON formatting for structured data logging
-   Optional inclusion of caller information (file and function name)

## Installation

### Using pip

To install PyLogger directly from GitHub, run:

```bash
pip install git+https://github.com/SudarshanVK/pylogger.git
```

### Using Poetry

To add PyLogger to your project using Poetry, run:

```bash
poetry add git+https://github.com/SudarshanVK/pylogger.git
```

## Usage

### Basic Usage

```python
from pylogger.logger import PyLogger

# Initialize the logger
logger = PyLogger("app.log")

# Use various logging methods
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

# Custom levels
logger.success("Operation successful")
logger.failed("Operation failed")
logger.message("Custom message")
```

### Logging with Additional Data

```python
data = {"user": "john_doe", "action": "login"}
logger.info("User action", data)
```

### Exception Logging

```python
try:
    1 / 0
except Exception:
    logger.exception()
```

## Configuration

### Controlling Caller Information

You can control whether to include caller information (file and function name) in your logs:

```python
# Create a logger with caller information included (default behavior)
logger = PyLogger("app.log")

# Create a logger without caller information
logger_without_caller = PyLogger("app.log", include_caller=False)

# Logs will include caller information
logger.info("This log includes caller info")

# Logs will not include caller information
logger_without_caller.info("This log doesn't include caller info")
```

The `include_caller` parameter allows you to globally set whether caller information should be included in logs for each logger instance. This can be useful for controlling log verbosity or for privacy concerns in production environments.

### Console Log Level

Set the `CONSOLE_LOG_LEVEL` environment variable to control console output:

```bash
CONSOLE_LOG_LEVEL=DEBUG python your_script.py
```

Valid levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

## Author

Sudarshan Vijaya Kumar
