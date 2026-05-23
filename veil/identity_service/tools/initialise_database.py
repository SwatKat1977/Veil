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
from weaver_framework.database.sqlite_interface import SqliteInterface
from veil.identity_service.database.account_repository import (
    AccountRepository)
from veil.identity_service.database.database_manager import (
    DatabaseManager)
from veil.identity_service.services.account_service import AccountService

DATABASE_FILENAME = "identity_LATEST.db"


def main() -> None:
    """Initialize and prepare the identity service database.

    This function configures application logging, creates the database
    interface and repository instances, and performs database
    initialization through the ``DatabaseManager``.

    The database schema and required tables are created or validated
    during initialization.

    Raises:
        sqlite3.Error: If a database operation fails during
            initialization.
    """

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    logger = logging.getLogger("veil.identity_service")

    sqlite_interface = SqliteInterface(
        logger,
        DATABASE_FILENAME
    )

    account_repository = AccountRepository(
        logger,
        sqlite_interface
    )
    account_service = AccountService(logger, account_repository)
    database_manager = DatabaseManager(
        logger,
        sqlite_interface,
        account_service)

    database_manager.initialise_database()

    logger.info("Database initialization complete")


if __name__ == "__main__":
    main()
