from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = "Bs3FNFYit_4WxxjIo9_enUoxZs1FxdVc5INeML7p7oLul0S_Lziw-YBc-oMxhQFNRlZ-wJpt0Qravg6smEunXQ=="
org = "solarcar"
bucket = "bucket"

with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)

    data = "mem,host=host1 used_percent=42"
    write_api.write(bucket, org, data)
    print('ok')
    # query = 'from(bucket: "bucket") |> range(start: -1h)'
    # tables = client.query_api().query(query, org=org)
    # for table in tables:
    #     for record in table.records:
    #         print(record)