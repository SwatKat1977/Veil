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
from quart import Quart
from veil.common.base_microservice import BaseMicroservice
from veil.common import LICENSE_TEXT, SERVICE_COPYRIGHT_TEXT, __version__
from veil.common.sqlite_interface import SqliteInterface, SqliteInterfaceException
from veil.identity_service.database.account_repository import AccountRepository
from veil.identity_service.database.database_manager import DatabaseManager
from veil.identity_service.routes import create_blueprints


class IdentityMicroservice(BaseMicroservice):
    """ VEIL Identity Service. """

    SERVICE_NAME = "veil.identityService"

    def __init__(self, quart_instance: Quart):
        super().__init__()
        self._quart_instance = quart_instance

    async def _initialise(self) -> bool:

        self.logger.info("VEIL Identity Microservice %s", __version__)
        self.logger.info(SERVICE_COPYRIGHT_TEXT)
        self.logger.info(LICENSE_TEXT)

        self._sqlite_interface = SqliteInterface(self.logger,
                                                 "databases/identity_LATEST.d_b")
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

        create_blueprints(self.logger)

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
