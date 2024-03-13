import mysql.connector
import csv
from datetime import datetime, timedelta
from tqdm import tqdm


logs_file="logs.csv"
table_name = "network_data"

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
    `Time` DATETIME,
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
    # Create a CSV DictReader object
    csv_reader = csv.DictReader(file)

    # Iterate through each row in the CSV file
    for row in tqdm(csv_reader, desc="Processing", unit="item"):
        # Each row is a dictionary with column names as keys
        insert_query = """
        INSERT INTO network_data 
        (Time, Duration, SrcDevice, DstDevice, Protocol, SrcPort, DstPort, SrcPackets, DstPackets, SrcBytes, DstBytes) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        seconds = int(row['Time'])
        base_datetime = datetime(2022, 1, 1)  # You can adjust this base datetime
        duration_timedelta = timedelta(seconds=seconds)
        result_datetime = base_datetime + duration_timedelta

        # Replace the following with your actual data
        data = (
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
        )

        cursor.execute(insert_query, data)
        connection.commit()

