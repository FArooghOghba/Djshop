from typing import TYPE_CHECKING, cast

import pytest

from src.djshop.tests.factories.product_class_factories import (
    OptionFactory, OptionGroupFactory,
)


if TYPE_CHECKING:
    from src.djshop.catalog.models import Option, OptionGroup


@pytest.fixture
def first_test_option_group() -> 'OptionGroup':

    """
    Pytest fixture that creates and returns an OptionGroup instance
    using OptionGroupFactory.

    This fixture uses the factory_boy library to generate an Option Group
    instance with random data for the 'title' field.
    The instance is saved to the test database.

    :returns: OptionGroup: An Option Group instance with random data.
    """

    test_option_group = OptionGroupFactory()
    return cast('OptionGroup', test_option_group)


@pytest.fixture
def first_test_option() -> 'Option':

    """
    Pytest fixture that creates and returns an Option instance
    using OptionFactory.

    This fixture uses the factory_boy library to generate an Option
    instance with random data for the 'title' field.
    The instance is saved to the test database.

    :returns: Option: An Option instance with random data.
    """

    test_option = OptionFactory()
    return cast('Option', test_option)


@pytest.fixture
def second_test_option() -> 'Option':

    """
    Pytest fixture that creates and returns an Option instance
    using OptionFactory.

    This fixture uses the factory_boy library to generate an Option
    instance with random data for the 'title' field.
    The instance is saved to the test database.

    :returns: Option: An Option instance with random data.
    """

    test_option = OptionFactory()
    return cast('Option', test_option)
