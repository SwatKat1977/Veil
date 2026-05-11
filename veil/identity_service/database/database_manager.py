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
from veil.common.sqlite_interface import SqliteInterface
from veil.identity_service.database import schema
from veil.identity_service.database.account_repository import AccountRepository


class DatabaseManager:
    """
    Handles database initialization, schema creation,
    schema versioning, and seed data.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self,
                 logger: logging.Logger,
                 sqlite_interface: SqliteInterface,
                 account_repository: AccountRepository) -> None:

        self._logger = logger.getChild(__name__)
        self._sqlite = sqlite_interface
        self._account_repository = account_repository

    def initialise_database(self) -> None:
        """
        Initialise the identity service database.
        """

        self._logger.info("Initialising identity service database")

        self._create_tables()
        self._create_indexes()
        self._initialise_schema_version()
        self._seed_default_roles()
        self._seed_default_admin_account()

        self._logger.info("Identity service database initialized")

    def _create_tables(self) -> None:
        """
        Create all database tables.
        """

        self._logger.debug("Creating database tables")

        for query in schema.TABLE_SCHEMA_QUERIES:
            self._sqlite.run_query(query, commit=True)

    def _create_indexes(self) -> None:
        """
        Create all database indexes.
        """

        self._logger.debug("Creating database indexes")

        for query in schema.INDEX_SCHEMA_QUERIES:
            self._sqlite.run_query(query, commit=True)

    def _initialise_schema_version(self) -> None:
        """
        Ensure schema version metadata exists.
        """

        result = self._sqlite.run_query(schema.GET_SCHEMA_VERSION,
                                        fetch_one=True)

        if result:
            self._logger.debug("Schema version already initialized: %s",
                               result[0])
            return

        self._logger.debug("Setting schema version to %s",
                           schema.SCHEMA_VERSION)

        self._sqlite.insert_query(schema.INSERT_SCHEMA_VERSION,
                                  (schema.SCHEMA_VERSION,))

    def _seed_default_roles(self) -> None:
        """
        Insert default system roles.
        """

        self._logger.debug("Seeding default roles")

        for role_name, description in schema.DEFAULT_ROLES:
            self._sqlite.insert_query(
                schema.INSERT_ROLE,
                (role_name, description))

    def _seed_default_admin_account(self) -> None:
        """
        Create the default administrator account if one does not exist.
        """

        admin_email = "admin@veil.local"
        admin_password = "admin"

        existing_account = self._account_repository.get_account_by_email(
            admin_email)

        if existing_account:
            self._logger.debug("Default admin account already exists")
            return

        self._logger.warning(
            "No administrator account detected, creating default admin account")

        #
        # WARNING:
        # Temporary/simple hashing for MVP only.
        # Replace with bcrypt/argon2 later.
        #
        password_hash = hashlib.sha256(admin_password.encode("utf-8")).hexdigest()

        account_id = self._account_repository.create_account(
            email_address=admin_email,
            display_name="admin",
            password_hash=password_hash,
            is_validated=True,
            is_disabled=False)

        if account_id is None:
            raise RuntimeError("Failed to create default admin account")

        role_id = self._account_repository.get_role_id("admin")

        if role_id is None:
            raise RuntimeError("Admin role missing from database")

        self._account_repository.assign_role(account_id, role_id)

        self._logger.warning("Default admin account created "
                             "(email=%s password=%s)",
                             admin_email,
                             admin_password)
