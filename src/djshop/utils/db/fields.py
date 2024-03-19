from typing import Any

import django_stubs_ext
from django.db.models import CharField


django_stubs_ext.monkeypatch()


class UpperCaseCharField(CharField[str, str]):

    """
    A custom CharField that stores and returns values in uppercase.

    This field inherits from Django's CharField and ensures that
    all values stored in the database and returned by the model
    are converted to uppercase.

    :param *args: Variable length argument list.
    :param **kwargs: Arbitrary keyword arguments.

    :returns str: The value stored in uppercase.
    """

    def from_db_value(self, value: Any, *args: Any, **kwargs: Any) -> str:

        """
        Convert the value retrieved from the database to uppercase.

        :param: value (Any): The value retrieved from the database.
        :param: *args: Variable length argument list.
        :param: **kwargs: Arbitrary keyword arguments.

        :returns str: The value converted to uppercase.
        """

        return self.to_python(value)

    def to_python(self, value: Any) -> str | Any:

        """
        Convert the provided value to uppercase.

        :param: value (Any): The value to be converted to uppercase.

        :returns: str: The value converted to uppercase, or
        the original value if it's not a string.
        """

        field_value = super().to_python(value)
        if isinstance(field_value, str):
            return field_value.upper()

        return field_value
