import logging
import uuid
from typing import Any
from veil.identity_service.database import schema
from veil.common.sqlite_interface import SqliteInterface


class AccountRepository:

    def __init__(self,
                 logger: logging.Logger,
                 sqlite_interface: SqliteInterface) -> None:

        self._logger = logger.getChild(__name__)
        self._sqlite = sqlite_interface

    def create_account(self,
                       email_address: str,
                       display_name: str,
                       password_hash: str,
                       is_validated: bool = False,
                       is_disabled: bool = False) -> int | None:
        """
        Create a new account.

        Returns:
            The inserted database account ID.
        """

        return self._sqlite.insert_query(
            schema.INSERT_ACCOUNT,
            (
                str(uuid.uuid4()),
                email_address,
                display_name,
                password_hash,
                int(is_validated),
                int(is_disabled)))

    def get_account_by_email(
            self,
            email_address: str) -> tuple[Any, ...] | tuple:
        """
        Fetch an account by email address.
        """

        return self._sqlite.run_query(
            schema.GET_ACCOUNT_BY_EMAIL,
            (email_address,),
            fetch_one=True)

    def get_account_by_user_id(
            self,
            user_id: str) -> tuple[Any, ...] | tuple:
        """
        Fetch an account by public user ID.
        """

        return self._sqlite.run_query(
            schema.GET_ACCOUNT_BY_USER_ID,
            (user_id,),
            fetch_one=True)

    def get_role_id(self, role_name: str) -> int | None:
        """
        Get a role ID from a role name.
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
        """
        Assign a role to an account.
        """

        self._sqlite.insert_query(schema.INSERT_ACCOUNT_ROLE,
                                  (account_id, role_id))
