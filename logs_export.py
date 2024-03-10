import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

logs_file = "logs.txt"
bucket="bucket"
token = os.environ.get("INFLUXDB_TOKEN")
org = "org"
url = "http://localhost:8086"
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

def convert_to_number(value):
    try:
        number_value = float(value)
        return number_value
    except ValueError:
        return value
    
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
                    if column in ["Time", "Duration", "SrcPackets", "DstPackets", "SrcBytes", "DstBytes"]:
                        value = convert_to_number(value)
                    point = point.field(column, value)
                print(point)
                write_api.write(bucket=bucket, org="org", record=point)

if __name__ == "__main__":
    main()

