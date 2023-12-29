from typing import Dict, Optional


class ApplicationError(Exception):

    """
    An error that occurs during the execution of an application.
    """

    def __init__(
            self, message: str, extra: Optional[Dict[str, str]] = None
    ) -> None:

        """
        Initializes a new instance of the ApplicationError class.

        :param message (str): A string that describes the error.
            extra (dict, optional): A dictionary that contains additional
                information about the error, Defaults to None.
        :return: None
        """

        super().__init__(message)

        self.message = message
        self.extra = extra or {}
