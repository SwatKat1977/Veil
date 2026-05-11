import logging
from veil.common.sqlite_interface import SqliteInterface
from veil.identity_service.database.account_repository import (
    AccountRepository)
from veil.identity_service.database.database_manager import (
    DatabaseManager)


DATABASE_FILENAME = "identity.db"


def main() -> None:

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

    database_manager = DatabaseManager(
        logger,
        sqlite_interface,
        account_repository
    )

    database_manager.initialise_database()

    logger.info("Database initialization complete")


if __name__ == "__main__":
    main()
