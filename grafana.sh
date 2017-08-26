#!/bin/bash

echo "Starting Grafana"
service grafana-server start

sleep 20

# add opentsdb datasource 
if [ ! -f /opt/datasource_created.txt ]; then
  echo "Creating opentsdb datasource in Grafana."
  curl 'http://admin:admin@127.0.0.1:3000/api/datasources' -X POST -H 'Content-Type: application/json;charset=UTF-8' --data-binary '{"name":"localOpenTSDB","type":"opentsdb","url":"http://127.0.0.1:4242","access":"proxy","isDefault":true}'
  touch /opt/datasource_created.txt

  curl 'http://admin:admin@127.0.0.1:3000/api/dashboards/db' -X POST -H 'Content-Type: application/json;charset=UTF-8' -d @/opt/dashboards/thermostat_overview.json
  curl 'http://admin:admin@127.0.0.1:3000/api/dashboards/db' -X POST -H 'Content-Type: application/json;charset=UTF-8' -d @/opt/dashboards/smoke_co_alarms.json
fi

