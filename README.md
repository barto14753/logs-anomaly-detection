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
```

### Grafana

Grafana on [localhost:3000](http://localhost:3000)

## Task 2

Analyze logs to detect and classify cyber attack
