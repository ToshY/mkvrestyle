class MKVmergeError(Exception):
    """
    Custom exception class for MKVmerge-related errors.

    This exception is raised when MKVmerge fails with a non-zero exit code.

    Attributes:
        exit_code (int): The exit code of the failed MKVmerge process.
        message (str): The error message associated with the failure.

    Args:
        message (str): The error message associated with the failure.
        exit_code (int): The exit code of the failed MKVmerge process.
    """

    ERROR_MESSAGE = "MKVmerge failed with exit code `{exit_code}`: {message}."

    def __init__(self, message, exit_code):
        self.exit_code = exit_code
        self.message = self.ERROR_MESSAGE.format(message=message, exit_code=exit_code)
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ProcessError(Exception):
    """
    Custom exception class for process-related errors.

    This exception is raised when a process fails with a non-zero exit code.

    Attributes:
        exit_code (int): The exit code of the failed process.
        message (str): The error message associated with the failure.

    Args:
        message (str): The error message associated with the failure.
        exit_code (int): The exit code of the failed process.
    """

    ERROR_MESSAGE = "Process failed with exit code `{exit_code}`: {message}."

    def __init__(self, message, exit_code):
        self.exit_code = exit_code
        self.message = self.ERROR_MESSAGE.format(message=message, exit_code=exit_code)
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidFontNameError(Exception):
    """
    Exception raised when an invalid font name is provided.

    This exception is raised when an invalid font name is provided.

    Attributes:
        message (str): The error message.

    """

    ERROR_MESSAGE = "Invalid font name `{font_name}` provided. Please provide and empty string or valid font name."

    def __init__(self, message):
        self.message = self.ERROR_MESSAGE.format(font_name=message)
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidFontSubstituteOptionError(Exception):
    """
    Exception raised when an invalid font substitution option is provided.

    This exception is raised when an invalid  font substitution option is provided.

    Attributes:
        message (str): The error message.

    """

    ERROR_MESSAGE = (
        "Invalid font substitution option `{option}` provided. Please provide `all` (replace everything) "
        "or `main` (dialogue font)."
    )

    def __init__(self, message):
        self.message = self.ERROR_MESSAGE.format(option=message)
        super().__init__(self.message)

    def __str__(self):
        return self.message


class FontNotFoundError(Exception):
    """
    Exception raised when the font was not found on either the filesystem or extracted attachment from the source file.

    This exception is raised when the font was not found on either the filesystem or extracted attachment from the
    source file.

    Attributes:
        message (str): The error message.

    """

    ERROR_MESSAGE = (
        "The font `{font_name}` was not found on either the filesystem or as an extracted attachment from the "
        "source file."
    )

    def __init__(self, message):
        self.message = self.ERROR_MESSAGE.format(font_name=message)
        super().__init__(message)

    def __str__(self):
        return self.message


class InvalidSubtitleFormatLines(Exception):
    """
    Exception raised when the subtitle file contains more than 2 'Format' lines in total.

    This exception is raised when the subtitle file contains more than 2 'Format' lines in total.

    Attributes:
        message (str): The error message.

    """

    ERROR_MESSAGE = "The original subtitle file contains more than 2 `Format` lines: {format_lines} total."

    def __init__(self, message):
        self.message = self.ERROR_MESSAGE.format(format_lines=message)
        super().__init__(self.message)

    def __str__(self):
        return self.message


class SubtitleNotFoundError(Exception):
    """
    Exception raised when no subtitle stream was found in the video file.

    This exception is raised when no subtitle stream was found in the video file.

    Attributes:
        message (str): The error message.

    """

    ERROR_MESSAGE = (
        "No subtitle stream was found for input file `{input_file}`. Make sure the file has at least 1 "
        "subtitle stream."
    )

    def __init__(self, message):
        self.message = self.ERROR_MESSAGE.format(input_file=message)
        super().__init__(self.message)

    def __str__(self):
        return self.message


class SubtitleCodecError(Exception):
    """
    Custom exception class for subtitle codec-related errors.

    This exception is raised when an invalid subtitle codec is provided.

    Attributes:
        message (str): The error message associated with the failure.

    Args:
        message (str): The error message associated with the failure.
    """

    ERROR_MESSAGE = "Invalid subtitle codec `{codec}` provided."

    def __init__(self, message):
        self.message = self.ERROR_MESSAGE.format(codec=message)
        super().__init__(self.message)

    def __str__(self):
        return self.message
