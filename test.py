from truckersmp import TruckersMP
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG,
                    format="[%(asctime)s:%(levelname)s:%(name)s:%(module)s:%(funcName)s:%(lineno)s] %(message)s",
                    datefmt="%d-%b-%y %H:%M:%S"
                    )

loop = asyncio.get_event_loop()


async def main():
    truckersmp = TruckersMP()
    servers = await truckersmp.get_servers()
    for server in servers:
        print(server.name)


if __name__ == "__main__":
    loop.run_until_complete(main())
