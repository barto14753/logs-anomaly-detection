import mysql.connector
import csv
from datetime import datetime, timedelta
from tqdm import tqdm
import random


logs_file="new_logs.csv"
table_name = "network_data"
BULK_SIZE = 500000
base_datetime = datetime(2024, 3, 13)

# Replace these with your actual MySQL database credentials
db_config = {
    "host": "localhost",
    "user": "user",
    "password": "password",
    "database": "logs",
}

# Connect to MySQL
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

try:
    drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
    cursor.execute(drop_table_query)
    connection.commit()
except Exception as ex:
    print("Drop table failed: {ex}")

# Create the network_data table
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    `time` DATETIME,
    `Duration` BIGINT,
    `SrcDevice` VARCHAR(255),
    `DstDevice` VARCHAR(255),
    `Protocol` VARCHAR(50),
    `SrcPort` VARCHAR(50),
    `DstPort` VARCHAR(50),
    `SrcPackets` BIGINT,
    `DstPackets` BIGINT,
    `SrcBytes` BIGINT,
    `DstBytes` BIGINT
)
"""

cursor.execute(create_table_query)
print("Table created successfully.")


with open(logs_file, 'r') as file:
    csv_reader = csv.DictReader(file)
    insert_query = """
        INSERT INTO network_data 
        (time, Duration, SrcDevice, DstDevice, Protocol, SrcPort, DstPort, SrcPackets, DstPackets, SrcBytes, DstBytes) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = []

    # Generate fake attack data 
    for i in range(10000):
        seconds = random.randint(120000, 120100)
        duration_timedelta = timedelta(seconds=seconds)
        result_datetime = base_datetime + duration_timedelta

        data.append((
            result_datetime,
            random.randint(1000, 10000),
            "src", 
            "dst", 
            "tcp", 
            "src_port", 
            "dst_port", 
            random.randint(300000000, 500000000),
            random.randint(300000000, 500000000),
            random.randint(60000000000, 100000000000),
            random.randint(60000000000, 100000000000)
        ))


    i = 0
    for row in tqdm(csv_reader, desc="Processing", unit="item"):
        seconds = int(row['Time'])
        duration_timedelta = timedelta(seconds=seconds)
        result_datetime = base_datetime + duration_timedelta

        try:
            data.append((
                result_datetime, 
                int(row['Duration']), 
                row['SrcDevice'], 
                row['DstDevice'], 
                row['Protocol'], 
                row['SrcPort'], 
                row['DstPort'], 
                int(row['SrcPackets']), 
                int(row['DstPackets']), 
                int(row['SrcBytes']), 
                int(row['DstBytes'])
            ))
        except Exception as ex:
            print(f"Exception occurred: {ex}")

        # Split insertion to many bulks to meet packet size limit
        if len(data) == BULK_SIZE:
            cursor.executemany(insert_query, data)
            connection.commit()
            data = []

