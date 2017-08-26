#!/bin/bash

echo "Starting tCollector"
sleep 60
python tcollector-1.3.2/tcollector.py -H localhost -p 4242 -c /opt/home_collectors/ -v


