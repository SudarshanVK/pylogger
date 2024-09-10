from unittest.mock import patch

import pytest

from pylogger.pylogger import LogLevel, PyLogger


# Fixture to create and clean up a PyLogger instance for each test
@pytest.fixture
def logger(tmp_path):
    log_file = tmp_path / "test_log.txt"
    yield PyLogger(str(log_file))
    # The tmp_path fixture will automatically clean up after the test


# Test that PyLogger maintains a singleton instance
def test_singleton_instance(logger):
    logger2 = PyLogger("another_log.txt")
    assert logger is logger2


# Test all standard log levels to ensure they call the underlying logger correctly
def test_log_levels(logger):
    with patch.object(logger.logger, "log") as mock_log:
        logger.debug("Debug message")
        mock_log.assert_called_with(LogLevel.DEBUG.value, "Debug message")

        logger.info("Info message")
        mock_log.assert_called_with(LogLevel.INFO.value, "Info message")

        logger.warning("Warning message")
        mock_log.assert_called_with(LogLevel.WARNING.value, "Warning message")

        logger.error("Error message")
        mock_log.assert_called_with(LogLevel.ERROR.value, "Error message")

        logger.critical("Critical message")
        mock_log.assert_called_with(LogLevel.CRITICAL.value, "Critical message")


# Test logging with additional data (dict) is correctly formatted
def test_log_with_data(logger):
    with patch.object(logger.logger, "log") as mock_log:
        data = {"key": "value"}
        logger.info("Info with data", data)
        expected_message = 'Info with data -\n{\n    "key": "value"\n}'
        mock_log.assert_called_with(LogLevel.INFO.value, expected_message)


# Test the success log method calls console.print
@patch("pylogger.pylogger.console.print")
def test_success_log(mock_print, logger):
    logger.success("Success message")
    mock_print.assert_called()


# Test the failed log method calls console.print
@patch("pylogger.pylogger.console.print")
def test_failed_log(mock_print, logger):
    logger.failed("Failed message")
    mock_print.assert_called()


# Test the message log method calls console.print
@patch("pylogger.pylogger.console.print")
def test_message_log(mock_print, logger):
    logger.message("Custom message")
    mock_print.assert_called()


# Test that including caller information works correctly
def test_include_caller(logger):
    logger.include_caller = True
    with patch.object(
        logger,
        "get_caller_function",
        return_value="test_file.py::test_function",
    ):
        with patch.object(logger.logger, "log") as mock_log:
            logger.info("Info with caller")
            mock_log.assert_called_with(
                LogLevel.INFO.value,
                "test_file.py::test_function | Info with caller",
            )


# Test that exception logging calls console.print_exception
@patch("pylogger.pylogger.console.print_exception")
def test_exception_logging(mock_print_exception, logger):
    logger.exception()
    mock_print_exception.assert_called_with(show_locals=False)


# Test that get_timestamp returns a string in the correct format
def test_get_timestamp(logger):
    timestamp = logger.get_timestamp()
    assert len(timestamp) == 17  # Format: "dd-mm-yy HH:MM:SS"


# Test that get_caller_function returns a non-empty string with expected format
def test_get_caller_function(logger):
    caller = logger.get_caller_function()
    assert caller != "Unknown"
    assert "::" in caller
