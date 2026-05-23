"""
Copyright 2026 Veil Development Team

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import logging
import uuid
from typing import Any
from weaver_framework.database.sqlite_interface import SqliteInterface
from veil.identity_service.database import schema
from veil.identity_service.models.account_creation_result import \
    AccountCreationResult


class AccountRepository:
    """Repository for account-related database operations.

    This repository provides methods for creating, retrieving,
    and managing account records and account role assignments
    within the identity service database.
    """

    def __init__(self,
                 logger: logging.Logger,
                 sqlite_interface: SqliteInterface) -> None:
        """Initialize the account repository.

        Args:
            logger: Parent logger instance used to create a
                repository-specific logger.
            sqlite_interface: SQLite interface instance used for
                database interactions.
        """
        self._logger = logger.getChild(__name__)
        self._sqlite = sqlite_interface

    def create_account(self,
                       email_address: str,
                       display_name: str,
                       password_hash: str,
                       is_validated: bool = False,
                       is_disabled: bool = False) -> \
            AccountCreationResult | None:
        """Create a new account record.

        Args:
            email_address: Email address associated with the account.
            display_name: Public display name for the account.
            password_hash: Securely hashed account password.
            is_validated: Whether the account has been validated.
            is_disabled: Whether the account is disabled.

        Returns:
            Account creation metadata containing both the
            internal database ID and public user ID if the
            insert succeeds, otherwise None.
        """
        # pylint: disable=too-many-positional-arguments, too-many-arguments

        unique_user_id: str = str(uuid.uuid4())
        account_id = self._sqlite.insert_query(
            schema.INSERT_ACCOUNT,
            (
                unique_user_id,
                email_address,
                display_name,
                password_hash,
                int(is_validated),
                int(is_disabled)))

        if account_id is None:
            return None

        return AccountCreationResult(
            id=account_id,
            user_id=unique_user_id)

    def get_account_by_email(
            self,
            email_address: str) -> tuple[Any, ...] | tuple:
        """Fetch an account by email address.

        Args:
            email_address: Email address associated with the account.

        Returns:
            A tuple containing the account record if found,
            otherwise an empty tuple.
        """
        return self._sqlite.run_query(
            schema.GET_ACCOUNT_BY_EMAIL,
            (email_address,),
            fetch_one=True)

    def get_account_by_user_id(
            self,
            user_id: str) -> tuple[Any, ...] | tuple:
        """Fetch an account by public user ID.

        Args:
            user_id: Public UUID associated with the account.

        Returns:
            A tuple containing the account record if found,
            otherwise an empty tuple.
        """
        return self._sqlite.run_query(
            schema.GET_ACCOUNT_BY_USER_ID,
            (user_id,),
            fetch_one=True)

    def get_role_id(self, role_name: str) -> int | None:
        """Retrieve a role ID from a role name.

        Args:
            role_name: Name of the role to retrieve.

        Returns:
            The database role ID if the role exists,
            otherwise None.
        """
        result = self._sqlite.run_query(
            schema.GET_ROLE_ID_BY_NAME,
            (role_name,),
            fetch_one=True)

        if not result:
            return None

        return result[0]

    def assign_role(self,
                    account_id: int,
                    role_id: int) -> None:
        """Assign a role to an account.

        Args:
            account_id: Internal database account ID.
            role_id: Internal database role ID.
        """
        self._sqlite.insert_query(schema.INSERT_ACCOUNT_ROLE,
                                  (account_id, role_id))

    def email_address_exists(self, email_address: str) -> bool:
        """Check whether an email address already exists.

        Args:
            email_address: Email address to check.

        Returns:
            True if the email address already exists,
            otherwise False.
        """
        result = self._sqlite.run_query(schema.CHECK_EMAIL_ADDRESS_EXISTS,
                                        (email_address,),
                                        fetch_one=True)
        return bool(result)

    def display_name_exists(self, display_name: str) -> bool:
        """Check whether a display name already exists.

        Args:
            display_name: Display name to check.

        Returns:
            True if the display name already exists,
            otherwise False.
        """
        result = self._sqlite.run_query(schema.CHECK_DISPLAY_NAME_EXISTS,
                                        (display_name,),
                                        fetch_one=True)
        return bool(result)
