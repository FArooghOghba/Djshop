import pytest
from django.db import IntegrityError

from src.djshop.catalog.models import Option, OptionGroup, OptionGroupValues


pytestmark = pytest.mark.django_db


def test_create_option_group_return_success() -> None:

    """
    Test creating an OptionGroup instance.
    :return: None
    """

    test_option_group_title = "Test Option Group"
    test_option_group = OptionGroup.objects.create(title=test_option_group_title)

    get_option_group = OptionGroup.objects.get(slug=test_option_group.slug)
    assert get_option_group.title == test_option_group_title


def test_create_option_group_values_return_success(
    first_test_option_group: 'OptionGroup'
) -> None:

    """
    Test creating an OptionGroupValues instance associated with an OptionGroup.

    :param first_test_option_group: A fixture providing the option group queryset.
    :return: None
    """

    test_option_group_value_title = "Test Option Group Value"
    test_option_group_value = OptionGroupValues.objects.create(
        title=test_option_group_value_title, option_group=first_test_option_group
    )

    get_option_group_values = OptionGroupValues.objects.get(
        pk=test_option_group_value.id
    )
    assert get_option_group_values.title == test_option_group_value_title


def test_create_option_group_values_without_option_group_return_error() -> None:

    """
    Test attempting to create an OptionGroupValues instance without
    specifying an OptionGroup.
    """

    # Attempting to create an option group value without a group
    # should raise IntegrityError
    with pytest.raises(IntegrityError):
        OptionGroupValues.objects.create(title="Test Option Group Value")


def test_create_option_return_success() -> None:

    """
    Test creating an Option instance.
    """

    test_option_title = "Test Option"
    test_option = Option.objects.create(title=test_option_title)

    get_option = Option.objects.get(slug=test_option.slug)
    assert get_option.title == test_option_title
    assert get_option.slug == 'test-option'
    assert get_option.type == 'text'
    assert get_option.required is False


def test_create_option_with_option_group_return_success(
    first_test_option_group: 'OptionGroup'
) -> None:

    """
    Test creating an Option instance associated with an OptionGroup.

    :param first_test_option_group: A fixture providing the option group queryset.
    :return: None
    """

    test_option_title = "Test Option"
    test_option = Option.objects.create(
        title=test_option_title, group=first_test_option_group
    )

    get_option = Option.objects.get(slug=test_option.slug)
    assert get_option.group == first_test_option_group


def test_create_option_without_option_group_return_success() -> None:

    """
    Test creating an Option instance without specifying an OptionGroup.
    """

    test_option_title = "Test Option"
    test_option = Option.objects.create(title=test_option_title)
    assert test_option.group is None
