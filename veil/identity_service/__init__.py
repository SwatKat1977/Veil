import asyncio
import sys
from quart import Quart
from veil.identity_service.identity_microservice import IdentityMicroservice

# Quart application instance
app = Quart(__name__)

service = IdentityMicroservice(app)


@app.before_serving
async def startup() -> None:
    """
    Code executed before Quart has began serving http requests.

    returns:
        None
    """
    if not await service.initialise():
        raise RuntimeError("Failed to initialise identity service")

    app.service_task = asyncio.ensure_future(service.run())


@app.after_serving
async def shutdown() -> None:
    """
    Code executed after Quart has stopped serving http requests.

    returns:
        None
    """
    await service.stop()
