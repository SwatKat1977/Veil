import asyncio
from veil.common.base_microservice import BaseMicroservice
from veil.common import LICENSE_TEXT, SERVICE_COPYRIGHT_TEXT, __version__


class IdentityMicroservice(BaseMicroservice):
    """ ITEMS Accounts Service """

    def __init__(self, quart_instance):
        super().__init__()
        self._quart_instance = quart_instance

    async def _initialise(self) -> bool:

        self._logger.info("VEIL Identity Microservice %s", __version__)
        self._logger.info(SERVICE_COPYRIGHT_TEXT)
        self._logger.info(LICENSE_TEXT)

        return True

    async def _create_tasks(self) -> list[asyncio.Task]:
        """ Create and return the service's background tasks. """
        return [
            asyncio.create_task(self._wait_forever())
        ]

    async def _shutdown(self):
        """ Application shutdown. """

    async def _wait_forever(self) -> None:
        await self.shutdown_event.wait()
