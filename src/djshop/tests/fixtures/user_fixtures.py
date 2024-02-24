from typing import TYPE_CHECKING, Dict, cast

import pytest

from src.djshop.tests.factories.user_factories import BaseUserFactory


if TYPE_CHECKING:
    from src.djshop.users.models import BaseUser


@pytest.fixture
def first_test_user_payload() -> Dict[str, str]:

    """
    Fixture for creating a test user instance.

    This fixture uses the `BaseUserFactory` factory
    to create a test user instance. The created user
    can be used in tests to simulate a user with predefined
    attributes for testing various scenarios.

    :return: a dict test user payload
    """

    return BaseUserFactory.create_payload()


@pytest.fixture
def first_test_superuser() -> 'BaseUser':

    """
    Fixture for creating a test superuser instance.

    This fixture uses the `BaseUserFactory` factory
    to create a test superuser instance. The created user
    can be used in tests to simulate a user with predefined
    attributes for testing various scenarios.

    :return: a test user instance
    """

    return BaseUserFactory.create_superuser()


@pytest.fixture
def first_test_user() -> 'BaseUser':

    """
    Fixture for creating a test user instance.

    This fixture uses the `BaseUserFactory` factory
    to create a test user instance. The created user
    can be used in tests to simulate a user with predefined
    attributes for testing various scenarios.

    :return: a test user instance
    """

    return cast('BaseUser', BaseUserFactory())


@pytest.fixture
def second_test_user() -> 'BaseUser':

    """
    Fixture for creating a test user instance.

    This fixture uses the `BaseUserFactory` factory
    to create a test user instance. The created user
    can be used in tests to simulate a user with predefined
    attributes for testing various scenarios.

    :return: a test user instance
    """

    return cast('BaseUser', BaseUserFactory())


@pytest.fixture
def third_test_user() -> 'BaseUser':

    """
    Fixture for creating a test user instance.

    This fixture uses the `BaseUserFactory` factory
    to create a test user instance. The created user
    can be used in tests to simulate a user with predefined
    attributes for testing various scenarios.

    :return: a test user instance
    """

    return cast('BaseUser', BaseUserFactory())
