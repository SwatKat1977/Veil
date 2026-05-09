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
