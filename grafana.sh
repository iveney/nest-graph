#!/bin/bash

echo "Starting Grafana"
cd /opt/grafana-2.5.0
./bin/grafana-server web &

sleep 20

# add opentsdb datasource 
if [ ! -f /opt/datasource_created.txt ]; then
  echo "Creating opentsdb datasource in Grafana."
  curl 'http://admin:admin@127.0.0.1:3000/api/datasources' -X POST -H 'Content-Type: application/json;charset=UTF-8' --data-binary '{"name":"localOpenTSDB","type":"opentsdb","url":"http://127.0.0.1:4242","access":"proxy","isDefault":true}'
  touch /opt/datasource_created.txt
fi

