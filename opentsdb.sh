#!/bin/bash

echo "Wait 40 seconds for HBase to start"
sleep 40

# check if tables are created
if [ ! -f /opt/hbase_table_created.txt ]; then
  echo "Creating tables for tsdb."
  env COMPRESSION=GZ HBASE_HOME=/opt/hbase-0.94.27 /usr/share/opentsdb/tools/create_table.sh
  touch /opt/hbase_table_created.txt
fi
mkdir /tmp/opentsdb_cache
echo -e "tsd.core.auto_create_metrics = true\ntsd.http.cachedir = /tmp/opentsdb_cache" >> /etc/opentsdb/opentsdb.conf 

echo "Starting opentsdb"
/usr/share/opentsdb/bin/tsdb tsd


