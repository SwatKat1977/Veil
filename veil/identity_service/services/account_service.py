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

from argon2 import PasswordHasher
from veil.identity_service.database.account_repository import \
    AccountRepository
from veil.identity_service.models.account_creation_result import \
    AccountCreationResult


class AccountService:
    """Business logic related to account management."""
    # pylint: disable=too-few-public-methods

    def __init__(self,
                 logger: logging.Logger,
                 account_repository: AccountRepository) -> None:
        """Initialize the account service.

        Args:
            logger: Logger instance used for service logging.
            account_repository: Repository used for account persistence
                and retrieval operations.
        """

        self._logger = logger.getChild(__name__)
        self._account_repository = account_repository
        self._password_hasher: PasswordHasher = PasswordHasher()

    def create_account(self,
                       email_address: str,
                       display_name: str,
                       password: str,
                       is_validated: bool = False,
                       is_disabled: bool = False) -> \
            AccountCreationResult | None:
        """Create a new account.

        Generates a unique user identifier, hashes the provided password,
        and persists the account using the configured repository.

        Args:
            email_address: Email address associated with the account.
            display_name: Public display name for the account.
            password: Plain text password provided during account creation.
            is_validated: Indicates whether the account has already been
                validated.
            is_disabled: Indicates whether the account should be created
                in a disabled state.

        Returns:
            AccountCreationResult containing the created account ID and
            generated user ID if successful, otherwise None.
        """

        # pylint: disable=too-many-arguments, too-many-positional-arguments

        password_hash = self._password_hasher.hash(password)

        unique_user_id: str = str(uuid.uuid4())

        account_id: int | None = self._account_repository.create_account(
            user_id=unique_user_id,
            email_address=email_address,
            display_name=display_name,
            password_hash=password_hash,
            is_validated=is_validated,
            is_disabled=is_disabled)

        if account_id is None:
            return None

        return AccountCreationResult(
            id=account_id,
            user_id=unique_user_id)

    def assign_role(self,
                    account_id: int,
                    role_name: str) -> bool:
        """Assign a role to an account.

        Args:
            account_id: Database ID of the account receiving the role.
            role_name: Name of the role to assign.

        Returns:
            True if the role was successfully assigned, otherwise False
            if the role does not exist.
        """

        role_id = self._account_repository.get_role_id(role_name)

        if role_id is None:
            self._logger.error("Role '%s' does not exist",
                               role_name)
            return False

        self._account_repository.assign_role(account_id,
                                             role_id)

        return True

    def get_account_by_email(
            self,
            email_address: str) -> tuple[Any, ...] | tuple:
        return self._account_repository.get_account_by_email(
            email_address)

    def get_role_id(self, role_name: str) -> int | None:
        return self._account_repository.get_role_id(role_name)

    def assign_role(self,
                    account_id: int,
                    role_id: int) -> None:
        return self._account_repository.assign_role(account_id, role_id)

    def email_address_exists(self, email_address: str) -> bool:
        return self._account_repository.email_address_exists(email_address)

    def display_name_exists(self, display_name: str) -> bool:
        return self._account_repository.display_name_exists(display_name)
