import mysql.connector

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

# Create the network_data table
create_table_query = """
CREATE TABLE IF NOT EXISTS network_data (
    `Time` DATETIME,
    `Duration` INT,
    `SrcDevice` VARCHAR(255),
    `DstDevice` VARCHAR(255),
    `Protocol` VARCHAR(50),
    `SrcPort` VARCHAR(50),
    `DstPort` VARCHAR(50),
    `SrcPackets` INT,
    `DstPackets` INT,
    `SrcBytes` INT,
    `DstBytes` INT
)
"""

cursor.execute(create_table_query)
print("Table created successfully.")

