import asyncio
import platform
from bleak import BleakClient
from helper import discover_ble, get_services, explore_services

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

ADDRESS = (
    "30:E2:83:8D:73:F2"
    if platform.system() != "Darwin"
    else "C8EB12A2-5C82-46C5-DF75-BE26DD8BE02E"
)
custom_service_UUID = "0000FFE1-0000-1000-8000-00805F9B34FB"
msg = bytearray()

# def callback(sender, data):
#     print("{0}".format("".join(map(chr, data))))

token = "Bs3FNFYit_4WxxjIo9_enUoxZs1FxdVc5INeML7p7oLul0S_Lziw-YBc-oMxhQFNRlZ-wJpt0Qravg6smEunXQ=="
org = "solarcar"
bucket = "bucket"
url="http://localhost:8086"


def on_receive(sender, data):
    global msg
    global msg_decoded
    if len(data) == 20:
        if data[19] == 1:
            msg = msg + data[0:19]
    else:
        msg = msg + data
        msg_decoded = msg.decode()
        print(msg_decoded)
        data = string2float(msg_decoded)

        with InfluxDBClient(url=url, token=token, org=org) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)

            # data = "mem,host=host1 used_percent=%f" % (float(d))
            p = Point("car").\
                tag("CANBus", "telemetry").\
                field("battery", data[0])
            write_api.write(bucket, org, p)

            p = Point("car").\
                    tag("CANBus", "telemetry").\
                    field("speed", data[1])
            write_api.write(bucket, org, p)

            p = Point("car").\
                    tag("CANBus", "telemetry").\
                    field("temperature", data[2])
            write_api.write(bucket, org, p)

            print('DB written')

        msg = bytearray()


async def read(address, UUID, callback):
    async with BleakClient(address) as client:
        await client.start_notify(UUID, callback)
        await asyncio.sleep(50)
        await client.stop_notify(UUID)

def string2float(s):
    l = []
    for t in s.split():
        try:
            l.append(float(t))
        except ValueError:
            pass
    return l

if __name__ == '__main__':
    # asyncio.run(discover_ble())
    asyncio.run(read(ADDRESS, custom_service_UUID, on_receive))
