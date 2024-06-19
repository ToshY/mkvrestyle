class MKVmergeError(Exception):
    """
    Exception raised when MKVmerge identify or remux fails.

    This exception is raised when the MKVmerge command line tool encounters an error during the identification or
    remuxing of a media file.

    Attributes:
        message (str): The error message.

    """

    ERROR_MESSAGE = "An error occurred running the mkvmerge command: {error}."

    def __init__(self, message):
        self.message = self.ERROR_MESSAGE.format(error=message)
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
