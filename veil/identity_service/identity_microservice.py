import asyncio
from veil.common.base_microservice import BaseMicroservice
from veil.common import __version__


class IdentityMicroservice(BaseMicroservice):
    """ ITEMS Accounts Service """

    def __init__(self, quart_instance):
        super().__init__()
        self._quart_instance = quart_instance

    async def _initialise(self) -> bool:

        return True

        version_info: str = f"V{RELEASE_VERSION}-{BUILD_VERSION}{BUILD_TAG}"

        self._logger.info("ITEMS Gateway Microservice %s", version_info)
        self._logger.info(SERVICE_COPYRIGHT_TEXT)
        self._logger.info(LICENSE_TEXT)

        if not self._manage_configuration():
            return False

        self._logger.info("Setting logging level to %s",
                          Configuration().logging_log_level)
        self._logger.setLevel(Configuration().logging_log_level)

        if not self._metadata_handler.read_metadata_file():
            return False

        if not self._check_accounts_svc_api_status(version_info):
            return False

        if not self._check_cms_svc_api_status(version_info):
            return False

        self._quart_instance.register_blueprint(
            create_web_routes(self._logger,
                              self._metadata_handler,
                              self._sessions,
                              "/web"), url_prefix="/web")

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
