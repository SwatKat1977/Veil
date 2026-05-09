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
