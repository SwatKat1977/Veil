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
