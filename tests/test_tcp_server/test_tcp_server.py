import asyncio
import logging

logger = logging.getLogger(__name__)


async def handle_echo(reader, writer):
    data = await reader.read(1024)
    addr = writer.get_extra_info('peername')

    logger.info(f"Received {len(data)} bytes from {addr!r}")

    writer.write(data)
    await writer.drain()


async def main():
    server = await asyncio.start_server(
        handle_echo, '0.0.0.0', 8080)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    logger.info(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

logging.basicConfig(level=logging.INFO)
asyncio.run(main())
