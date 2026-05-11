import asyncio
import os
import signal

from hypercorn.asyncio import serve
from hypercorn.config import Config

from veil.identity_service import app, service


async def main() -> int:
    if not await service.initialise():
        await service.stop()
        return 1

    service_task = asyncio.create_task(service.run())

    shutdown_event = asyncio.Event()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            asyncio.get_running_loop().add_signal_handler(
                sig,
                shutdown_event.set
            )
        except NotImplementedError:
            # Windows fallback; CTRL+C still cancels asyncio.run().
            pass

    host = os.getenv("VEIL_IDENTITY_SERVICE_HOST", "127.0.0.1")
    port = int(os.getenv("VEIL_IDENTITY_SERVICE_PORT", "5050"))

    config = Config()
    config.bind = [f"{host}:{port}"]

    server_task = asyncio.create_task(
        serve(app, config, shutdown_trigger=shutdown_event.wait)
    )

    try:
        await server_task
    except KeyboardInterrupt:
        shutdown_event.set()
    finally:
        await service.stop()

        service_task.cancel()
        await asyncio.gather(service_task, return_exceptions=True)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(asyncio.run(main()))

    except KeyboardInterrupt:
        pass
