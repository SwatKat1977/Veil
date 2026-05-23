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
import hashlib
import logging
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
        """Initialize the account service."""

        self._logger = logger.getChild(__name__)
        self._account_repository = account_repository

    def create_account(self,
                       email_address: str,
                       display_name: str,
                       password: str,
                       is_validated: bool = False,
                       is_disabled: bool = False) -> \
            AccountCreationResult | None:
        """Create a new account."""
        # pylint: disable=too-many-arguments, too-many-positional-arguments


        #
        # WARNING:
        # Temporary/simple hashing for MVP only.
        # Replace with Argon2 later.
        #
        password_hash = hashlib.sha256(
            password.encode("utf-8")).hexdigest()

        return self._account_repository.create_account(
            email_address=email_address,
            display_name=display_name,
            password_hash=password_hash,
            is_validated=is_validated,
            is_disabled=is_disabled)
