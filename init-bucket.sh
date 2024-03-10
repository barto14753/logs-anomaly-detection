#!/bin/bash

until curl -s http://influxdb:8086/ping; do
  echo 'Waiting for InfluxDB to be available...'
  sleep 1
done

# Init bucket
influx setup --force -n mydb -r 1w -p bucket

echo 'Bucket initialized successfully.'
