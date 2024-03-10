import influxdb_client, os, time
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import time
from datetime import datetime, timezone

# Constants
logs_file = "logs.txt"
bucket="bucket"
token = os.environ.get("INFLUXDB_TOKEN")
org = "org"
url = "http://localhost:8086"

# API
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

def convert_to_number(value):
    try:
        number_value = float(value)
        return number_value
    except ValueError:
        return value

def convert_time(value):
    timestamp = int(time.time()) - 48 * 3600 + int(value)
    dt_object = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)
    formatted_time = dt_object.strftime("%Y-%m-%dT%H:%M:%SZ")
    print(formatted_time)
    return formatted_time


def main():
    with open(logs_file, 'r') as file:
        columns= None
        for line in file:
            if columns is None:
                columns = line.strip().split(",")
            else:
                data  = line.strip().split(",")
                point = Point("logs")
                for column, value in zip(columns, data):
                    if column in ["Duration", "SrcPackets", "DstPackets", "SrcBytes", "DstBytes"]:
                        value = convert_to_number(value)
                    elif column == "Time":
                        formatted_time = convert_time(value)
                        point = point.time(formatted_time)
                    point = point.field(column, value)
                print(point)
                write_api.write(bucket=bucket, org="org", record=point)

if __name__ == "__main__":
    main()

