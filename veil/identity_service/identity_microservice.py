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
import asyncio
from pathlib import Path
from quart import Quart
from weaver_framework.microservice.base_microservice import BaseMicroservice
from weaver_framework.database.sqlite_interface import (
    SqliteInterface, SqliteInterfaceException)
from weaver_framework.configuration_system.configuration_manager import (
    ConfigurationError)
from veil.common import LICENSE_TEXT, SERVICE_COPYRIGHT_TEXT, __version__
from veil.identity_service.database.account_repository import AccountRepository
from veil.identity_service.database.database_manager import DatabaseManager
from veil.identity_service.routes import create_blueprints
from veil.identity_service.configuration_layout import CONFIGURATION_LAYOUT
from veil.identity_service.identity_configuration import IdentityConfiguration
from veil.identity_service.routes.route_injections import RouteInjections


class IdentityMicroservice(BaseMicroservice):
    """ VEIL Identity Service. """

    SERVICE_NAME = "veil.identityService"

    CONFIG_FILE_ENV: str = "VEIL_IDENTITY_CONFIG_FILE"
    CONFIG_REQUIRED_ENV: str = "VEIL_IDENTITY_CONFIG_FILE_REQUIRED"

    def __init__(self, quart_instance: Quart):
        super().__init__()
        self._quart_instance = quart_instance

        self._sqlite_interface: SqliteInterface | None = None
        self._account_repository: AccountRepository | None = None
        self._database_manager: DatabaseManager | None = None
        self._config_manager: IdentityConfiguration = IdentityConfiguration()

    async def _initialise(self) -> bool:

        self.logger.info("VEIL Identity Microservice %s", __version__)
        self.logger.info(SERVICE_COPYRIGHT_TEXT)
        self.logger.info(LICENSE_TEXT)

        if not self._manage_configuration():
            return False

        self._logger.setLevel(self._config_manager.logging_log_level)

        db_filename: Path = Path(self._config_manager.backend_db_filename)

        if not db_filename.is_file():
            self.logger.error("Database file '%s' is missing!", db_filename)
            return False

        self._sqlite_interface = SqliteInterface(self.logger, db_filename)

        if not self._sqlite_interface.is_valid_database():
            self.logger.error("Database file '%s' is not a valid SQLite2 db",
                              db_filename)
            return False

        self._account_repository = AccountRepository(self.logger,
                                                     self._sqlite_interface)
        self._database_manager = DatabaseManager(self.logger,
                                                 self._sqlite_interface,
                                                 self._account_repository)
        try:
            self._sqlite_interface.ensure_valid()

        except SqliteInterfaceException as ex:
            self.logger.error("Failed to start database, reason: %s", ex)
            return False

        route_injections: RouteInjections = RouteInjections(
            self._logger, self._account_repository)
        self._quart_instance.register_blueprint(
            create_blueprints(route_injections))

        return True

    async def _create_tasks(self) -> list[asyncio.Task]:
        """ Create and return the service's background tasks. """
        return [
            asyncio.create_task(self._wait_forever())
        ]

    async def _shutdown(self) -> None:
        """ Application shutdown. """

    async def _wait_forever(self) -> None:
        await self.shutdown_event.wait()

    def _manage_configuration(self) -> bool:
        """
        Manage the service configuration.
        """
        error_status, required, config_file = self._check_for_configuration(
            self.CONFIG_FILE_ENV, self.CONFIG_REQUIRED_ENV)
        if error_status:
            self._logger.critical(error_status)
            return False

        self._config_manager.configure(CONFIGURATION_LAYOUT,
                                       config_file,
                                       required)

        try:
            self._config_manager.process_config()

        except (ValueError, ConfigurationError) as ex:
            self._logger.critical("Configuration error : %s", str(ex))
            return False

        self._logger.info("Configuration")
        self._logger.info("=============")

        self._logger.info("Configuration file required: %s",
                          "True" if required else "False")
        self._logger.info("Configuration file : %s",
                          "None" if not required else config_file)
        self._logger.info("[logging]")
        self._logger.info("=> Logging log level : %s",
                          self._config_manager.logging_log_level)
        self._logger.info("[Backend]")
        self._logger.info("=> Database filename : %s",
                          self._config_manager.backend_db_filename)

        return True
