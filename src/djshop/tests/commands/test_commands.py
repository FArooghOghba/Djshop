"""
Test custom Django management commands.
"""
from unittest.mock import MagicMock, patch

from django.core.management import call_command
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2Error


@patch(
    'src.djshop.common.management.commands.wait_for_db.Command.check'
)
class TestWaitForDBCommand:

    """Test cases for the wait_for_db management command."""

    def test_wait_for_db_command_is_ready(
            self, patched_check: MagicMock
    ) -> None:

        """
        Test that the wait_for_db command waits for the database
        to be ready if the database is already available.

        :param patched_check: Mocked check function
        :return: None
        """

        patched_check.return_value = True
        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_command_has_delay(
            self, patched_sleep: MagicMock, patched_check: MagicMock
    ) -> None:

        """
        Test that the wait_for_db command retries waiting for the database
        to be ready after encountering errors.

        :param patched_sleep: Mocked "time.sleep" function
        :param patched_check: Mocked check function
        :return: None
        """

        # Simulating 2 Psycopg2Errors followed by 3 OperationalErrors
        # before succeeding.
        patched_check.side_effect = [Psycopg2Error] * 2 + \
                                    [OperationalError] * 3 + \
                                    [True]

        call_command('wait_for_db')

        assert patched_check.call_count == 6
        patched_check.assert_called_with(databases=['default'])
