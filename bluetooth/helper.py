from bleak import BleakClient
from bleak import BleakScanner
import logging


async def discover_ble():
    devices = await BleakScanner.discover()
    for d in devices:
        # print(d)
        print(d.name + ": " + d.address)

async def get_services(address):
    async with BleakClient(address) as client:
        svcs = await client.get_services()
        print("Services:")
        for service in svcs:
            print(service)


async def explore_services(address):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    async with BleakClient(address) as client:
        logger.info(f"Connected: {client.is_connected}")

        for service in client.services:
            logger.info(f"[Service] {service}")
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = bytes(await client.read_gatt_char(char.uuid))
                        logger.info(
                            f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}"
                        )
                    except Exception as e:
                        logger.error(
                            f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {e}"
                        )

                else:
                    value = None
                    logger.info(
                        f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}"
                    )

                for descriptor in char.descriptors:
                    try:
                        value = bytes(
                            await client.read_gatt_descriptor(descriptor.handle)
                        )
                        logger.info(f"\t\t[Descriptor] {descriptor}) | Value: {value}")
                    except Exception as e:
                        logger.error(f"\t\t[Descriptor] {descriptor}) | Value: {e}")
