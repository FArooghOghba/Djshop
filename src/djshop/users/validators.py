from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

import re


def number_validator(password: str) -> None:

    """
    Validates that a password contains at least one number.

    :param: password (str): The password to validate.

    :raises: ValidationError: If the password does not contain a number.
    """

    regex = re.compile('[0-9]')
    if regex.search(password) is None:
        raise ValidationError(
            _("password must include number"),
            code="password_must_include_number"
        )


def letter_validator(password: str) -> None:

    """
    Validates that a password contains at least one letter.

    :param: password (str): The password to validate.

    :raises: ValidationError: If the password does not contain a letter.
    """

    regex = re.compile('[a-zA-Z]')
    if regex.search(password) is None:
        raise ValidationError(
            _("password must include letter"),
            code="password_must_include_letter"
        )


def special_char_validator(password: str) -> None:

    """
    Validates that a password contains at least one special character.

    :param: password (str): The password to validate.

    :raises: ValidationError: If the password does not contain a special character.
    """

    regex = re.compile('[@_!#$%^\'\"&*()<>?/|}{~:]')
    if regex.search(password) is None:
        raise ValidationError(
            _("password must include special char"),
            code="password_must_include_special_char"
        )
