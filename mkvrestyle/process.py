import subprocess as sp

from rich import print

from mkvrestyle.exception import MKVmergeError


class ProcessDisplay:
    """
    Class for displaying subprocess information on the console.

    Attributes:
        logger: The logger object used for logging information.
        process_exceptions: A dictionary mapping process names to corresponding exceptions.
        colors: A dictionary mapping status colors for the console display.
    """

    def __init__(self, logger):
        """
        Initializes a new instance of the ProcessDisplay class.

        Args:
            logger (Logger): The logger object used for logging messages.

        Initializes the following instance variables:
            - logger (Logger): The logger object used for logging messages.
            - process_exceptions (dict): A dictionary mapping process names to their corresponding exception classes.
            - colors (dict): A dictionary mapping color names to their corresponding color codes.
        """
        self.logger = logger
        self.process_exceptions = {
            "mkvmerge": MKVmergeError,
        }

        self.colors = {"ok": "green", "busy": "cyan"}

    def run(self, process, command, process_color="#F79EDE"):
        """
        Run a subprocess command and display information on the console.

        Args:
            process: The name of the process being executed.
            command: The command to be executed.
            process_color: The color used for display. Default is "#F79EDE".

        Returns:
            The response object from the subprocess execution.
        """
        print(
            f"> The following [{process_color}]{process}[/{process_color}] command will be executed:\r"
        )
        print(f"[{self.colors['ok']}]{' '.join(command)}[/{self.colors['ok']}]")
        print(
            f"\r> [{process_color}]{process}[/{process_color}] [{self.colors['busy']}]running...[/"
            f"{self.colors['busy']}]",
            end="\r",
        )

        response = sp.run(command, stdout=sp.PIPE, stderr=sp.PIPE)
        return_code = response.returncode
        if return_code == 0:
            print(
                f"> [{process_color}]{process}[/{process_color}] [{self.colors['ok']}]completed[/"
                f"{self.colors['ok']}]!\r\n"
            )
            return response

        if command[0] not in self.process_exceptions:
            exception = self.process_exceptions["custom"]
        else:
            exception = self.process_exceptions[command[0]]

        self.logger.critical(response)
        raise exception(
            "Process returned exit code `{return_code}`.\r\n\r\n"
            + response.stderr.decode("utf-8")
        )
