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
from typing import Any
from weaver_framework.database.sqlite_interface import SqliteInterface
from veil.identity_service.database import schema_session


class AccountSessionRepository:
    """Repository for managing account session records.

    This repository provides methods for creating and retrieving
    account session data stored in the SQLite database.

    Attributes:
        _logger (logging.Logger):
            Logger instance used for repository logging.
        _sqlite (SqliteInterface):
            SQLite interface used to execute database queries.
    """

    def __init__(self,
                 logger: logging.Logger,
                 sqlite_interface: SqliteInterface) -> None:
        """Initializes the account session repository.

        Args:
            logger (logging.Logger):
                Parent logger instance.
            sqlite_interface (SqliteInterface):
                SQLite interface used for database operations.
        """
        self._logger = logger.getChild(__name__)
        self._sqlite = sqlite_interface

    def create_session(self,
                       session_id: str,
                       account_id: int,
                       session_token: str,
                       created_at: str,
                       expires_at: str) -> int | None:
        """Creates a new account session record.

        Args:
            session_id (str):
                Unique identifier for the session.
            account_id (int):
                Identifier of the account associated with the session.
            session_token (str):
                Authentication token for the session.
            created_at (str):
                Timestamp indicating when the session was created.
            expires_at (str):
                Timestamp indicating when the session expires.

        Returns:
            int | None:
                The inserted row ID if the insert succeeds,
                otherwise ``None``.
        """
        # pylint: disable=too-many-arguments, too-many-positional-arguments
        return self._sqlite.insert_query(
            schema_session.INSERT_ACCOUNT_SESSION,
            (session_id,
             account_id,
             session_token,
             created_at,
             expires_at))

    def get_session_by_token(
            self,
            session_token: str) -> tuple[Any, ...] | tuple:
        """Retrieves an account session by its session token.

        Args:
            session_token (str):
                Session token associated with the account session.

        Returns:
            tuple[Any, ...] | tuple:
                A tuple containing the session record if found,
                otherwise an empty tuple.
        """
        return self._sqlite.run_query(
            schema_session.GET_SESSION_BY_TOKEN,
            (session_token,),
            fetch_one=True)
