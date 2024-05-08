import csv
from tqdm import tqdm
import random
import numpy as np

LOGS_FILE="logs.csv"

# Data
logs = list()
time = list()
duration = list()
src_devices = set()
dst_devices = set()
protocols = set()
src_ports = set()
dst_ports = set()
src_bytes = list()
dst_bytes = list()
src_packets = list()
dst_packets = list()

# Attack logs stats
NUMBER_OF_LOGS = 100000
ATTACK_DURATION = 300 # 5 minutes
ATTACKER_DEVICES = 1000
ATTACKED_DEVICES = 50
ATTACK_PROTOCOLS = 3
ATTACK_PORTS = 100
ATTACKED_PORTS = 10
MIN_MODIFIER = 1.5
MAX_MODIFIER = 2.5

def remove_zeros(data):
    return [x for x in data if x != 0]


with open(LOGS_FILE, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in tqdm(csv_reader, desc="Processing", unit="item"):
        try:
            time_ = int(row['Time'])
            duration_ = int(row['Duration'])
            src_bytes_ = int(row['SrcBytes'])
            dst_bytes_ = int(row['DstBytes'])
            src_packets_ = int(row['SrcPackets'])
            dst_packets_ = int(row['DstPackets'])
            src_device = row['SrcDevice']
            dst_device = row['DstDevice']
            protocol = row['Protocol']
            src_port = row['SrcPort']
            dst_port = row['DstPort']
            
            logs.append((time_, duration_, src_device, dst_device, protocol, src_port, dst_port, src_bytes_, dst_bytes_, src_packets_, dst_packets_))
            
            time.append(time_)
            duration.append(duration_)
            src_bytes.append(src_bytes_)
            dst_bytes.append(dst_bytes_)
            src_packets.append(src_packets_)
            dst_packets.append(dst_packets_)
            src_devices.add(src_device)
            dst_devices.add(dst_device)
            protocols.add(protocol)
            src_ports.add(src_port)
            dst_ports.add(dst_port)
        except Exception as e:
            print(e)
        
        # Remove all zeros from data
    time = remove_zeros(time)
    duration = remove_zeros(duration)
    src_bytes = remove_zeros(src_bytes)
    dst_bytes = remove_zeros(dst_bytes)
    src_packets = remove_zeros(src_packets)
    dst_packets = remove_zeros(dst_packets)

print(f"Unique src devices: {len(src_devices)}")
print(f"Unique dst devices: {len(dst_devices)}")
print(f"Unique protocols: {len(protocols)}")
print(f"Unique src ports: {len(src_ports)}")
print(f"Unique dst ports: {len(dst_ports)}")


print(f"Random src devices: {random.sample(sorted(src_devices), 3)}")
print(f"Random dst devices: {random.sample(sorted(dst_devices), 3)}")
print(f"Random protocols: {random.sample(sorted(protocols), 3)}")
print(f"Random src ports: {random.sample(sorted(src_ports), 3)}")
print(f"Random dst ports: {random.sample(sorted(dst_ports), 3)}")


print(f"Min time {np.min(time)} | Max time {np.max(time)} | Mean time {np.mean(time)} | Median time {np.median(time)}")
print(f"Min duration {np.min(duration)} | Max duration {np.max(duration)} | Mean duration {np.mean(duration)} | Median duration {np.median(duration)}")
print(f"Min src bytes {np.min(src_bytes)} | Max src bytes {np.max(src_bytes)} | Mean src bytes {np.mean(src_bytes)} | Median src bytes {np.median(src_bytes)}")
print(f"Min dst bytes {np.min(dst_bytes)} | Max dst bytes {np.max(dst_bytes)} | Mean dst bytes {np.mean(dst_bytes)} | Median dst bytes {np.median(dst_bytes)}")
print(f"Min src packets {np.min(src_packets)} | Max src packets {np.max(src_packets)} | Mean src packets {np.mean(src_packets)} | Median src packets {np.median(src_packets)}")
print(f"Min dst packets {np.min(dst_packets)} | Max dst packets {np.max(dst_packets)} | Mean dst packets {np.mean(dst_packets)} | Median dst packets {np.median(dst_packets)}")

# Get time of attack
start_time = np.random.randint(np.min(time), np.max(time) - ATTACK_DURATION)
end_time = start_time + ATTACK_DURATION
print("Start time: ", start_time)
print("End time: ", end_time)

# Get random src and dst devices, protocols, src and dst ports
src_devices = random.sample(sorted(src_devices), ATTACKER_DEVICES)
dst_devices = random.sample(sorted(dst_devices), ATTACKED_DEVICES)
protocols = random.sample(sorted(protocols), ATTACK_PROTOCOLS) 
src_ports = random.sample(sorted(src_ports), ATTACK_PORTS) 
dst_ports = random.sample(sorted(dst_ports), ATTACKED_PORTS)

def generate_range_with_repeats(start, end, num):
    return np.linspace(start, end, num, dtype=int)

max_duration = np.max(duration)
max_src_bytes = np.max(src_bytes)
max_dst_bytes = np.max(dst_bytes)
max_src_packets = np.max(src_packets)
max_dst_packets = np.max(dst_packets)

def get_random_value():
    return np.random.uniform(MIN_MODIFIER, MAX_MODIFIER)

for timestamp in generate_range_with_repeats(start_time, end_time, NUMBER_OF_LOGS):
    dur = int(max_duration * get_random_value())
    src_device = random.choice(src_devices)
    dst_device = random.choice(dst_devices)
    protocol = random.choice(protocols)
    src_port = random.choice(src_ports)
    dst_port = random.choice(dst_ports)
    src_byte = int(max_src_bytes * get_random_value())
    dst_byte = int(max_dst_bytes * get_random_value())
    src_packet = int(max_src_packets * get_random_value())
    dst_packet = int(max_dst_packets * get_random_value())
    attack_log = (timestamp, dur, src_device, dst_device, protocol, src_port, dst_port, src_byte, 0, src_packet, 0)
    logs.append(attack_log)
    # print(attack_log)


logs.sort(key=lambda x: x[0])

## Create new_logs.csv file and append logs to it
with open('new_logs.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow((
        "Time", 
        "Duration", 
        "SrcDevice", 
        "DstDevice", 
        "Protocol", 
        "SrcPort", 
        "DstPort", 
        "SrcPackets", 
        "DstPackets", 
        "SrcBytes", 
        "DstBytes"
    ))
    writer.writerows(logs)
