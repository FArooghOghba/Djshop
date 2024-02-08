import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def letter_validator(title: str) -> None:

    """
    Validates that a title contains at least 6 letters.

    :param: title (str): The title to validate.

    :raises: ValidationError: If the title does not contain a letter.
    """

    regex = re.compile(r'[a-zA-Z].*[a-zA-Z].*[a-zA-Z].*[a-zA-Z].*[a-zA-Z]')
    if regex.search(title) is None:
        raise ValidationError(
            _("title must include at least 6 letters"),
            code="title_must_include_6_letter"
        )
