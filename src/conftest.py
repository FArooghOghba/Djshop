"""
Conftest for tests
"""
from datetime import datetime
from typing import Generator

import pytest
from rest_framework.test import APIClient, APIRequestFactory


@pytest.fixture
def api_client() -> APIClient:

    """
    Fixture for creating an instance of the Django REST Framework's APIClient.
    :return: APIClient()
    """

    return APIClient()


@pytest.fixture
def api_request() -> APIRequestFactory:

    """
    Fixture for creating an instance of the APIRequestFactory.

    This fixture provides an instance of the APIRequestFactory,
    which is a utility class provided by Django REST Framework
    for creating API requests in tests.

    :return: APIRequestFactory: An instance of the APIRequestFactory.
    """

    return APIRequestFactory()


@pytest.fixture(autouse=True)
def time_tracker() -> Generator[None, None, None]:

    """
    Fixture for tracking the runtime of a test or a block of code.

    This fixture captures the start time before executing the test or
    the block of code, and calculates the elapsed time after the execution.
    It then prints the runtime in seconds.
    :return: runtime for how long it has taken to run the test.
    """

    tick = datetime.now()
    yield

    tock = datetime.now()
    diff = tock - tick
    print(f'\n runtime: {diff.total_seconds()}')


from src.djshop.tests.fixtures.catalog_fixtures import *  # noqa
