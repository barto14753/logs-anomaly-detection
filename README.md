# logs-anomaly-detection

[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)]()
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)

## Task 1

Prepare package of logs from application under cyber attack

### Run

```
# Run mysql and grafana
docker-compose up

# Run script to import logs data to database
python3 mysql_export.py

# Run script to generate attack logs
python3 attack_logs_generator.py
```

### Attack Logs Generation

The `attack_logs_generator.py` script is responsible for generating simulated attack logs. This script calculate statistics of the provided logs and based on them append newly generated logs simulating DDOS attack.

#### Parameters

You can modify the parameters of the `attack_logs_generator.py` inside script. Here's how you can do it:

- `NUMBER_OF_LOGS`: This parameter defines the total number of logs that will be generated by the script.
- `ATTACK_DURATION`: This parameter defines the duration of the cyber attack in seconds.
- `ATTACKER_DEVICES`: This parameter defines the number of devices that are performing the attack.
- `ATTACKED_DEVICES`: This parameter defines the number of devices that are being attacked.
- `ATTACK_PROTOCOLS`: This parameter defines the number of different protocols used in the attack.
- `ATTACK_PORTS`: This parameter defines the number of different ports from which the attack is being performed.
- `ATTACKED_PORTS`: This parameter defines the number of different ports that are being attacked.
- `MIN_MODIFIER` : This parameter defines the minimum value of the random modifier that is used to generate the logs.
- `MAX_MODIFIER` : This parameter defines the maximum value of the random modifier that is used to generate the logs.

### Grafana

Grafana on [localhost:3000](http://localhost:3000)

#### Add mysql datasource

![screencapture-localhost-3000-connections-datasources-edit-bdijk1g9mxkhsf-2024-04-12-22_15_46](https://github.com/barto14753/logs-anomaly-detection/assets/56938330/beadd532-712c-4840-bd5e-9f63c8b79a52)

#### Example dashboard

![screencapture-localhost-3000-explore-2024-04-12-22_38_00](https://github.com/barto14753/logs-anomaly-detection/assets/56938330/28577465-20f8-48da-b047-b94d76df112c)

## Task 2

Analyze logs to detect and classify cyber attack. Notebook analysis in `analysis/analysis.ipynb` based on logs provided from other team
