#!/usr/bin/python

import sys
import time
import nest
import json
import os.path

#from home_collectors.lib import utils

ROOT_METRIC = "nest"
CONFIG_FILE = '/opt/nest-config.json'

def get_config():
    if os.path.isfile(CONFIG_FILE):
        with open('/opt/nest-config.json') as json_data:
            nest_conf = json.load(json_data)

            config = {
                'collection_interval': 60,   # Seconds, how often to collect metric data
                'collection_filter': '.*',    # Filter to choose disks, .* will take all disks
                'client_id': nest_conf['client_id'],
                'client_secret': nest_conf['client_secret'],
                'access_token_cache_file': nest_conf['access_token_cache_file']
            }

            return config
    else:
        return None

def collect_all_devices(napi):
    for structure in napi.structures:
        ts = time.time()
        tags = {"structure":structure.name}
        away_val = {
            'home': 1,
            'away': 0,
            'unknown': -1,
        }[structure.away]
        printmetric("away", ts, away_val, tags)
        printmetric("num_thermostats", ts, structure.num_thermostats, tags)

        for device in structure.thermostats:
            tags = {"structure":structure.name, "device":device.name}
            metric_prefix = "thermostat."
            printmetric(metric_prefix + "temperature", ts, device.temperature, tags)
            printmetric(metric_prefix + "humidity", ts, device.humidity, tags)
            printmetric(metric_prefix + "target", ts, device.target, tags)
            printmetric(metric_prefix + "eco.temperature.low", ts, device.eco_temperature.low, tags)
            printmetric(metric_prefix + "eco.temperature.high", ts, device.eco_temperature.high, tags)

            online_val = {
                True: 1,
                False: 0
            }[device.online]
            printmetric(metric_prefix + "is_online", ts, online_val, tags)

            hvac_state_val = {
                'heating': 1,
                'off': 0,
                'cooling': -1,
            }[device.hvac_state]
            printmetric(metric_prefix + "hvac_state", ts, hvac_state_val, tags)

        for device in structure.smoke_co_alarms:
            tags = {"structure":structure.name, "device":device.name}
            metric_prefix = "smoke_co_alarm."

            status_map = {
                'ok': 0,
                'warning': 1,
                'emergency': 2
            }
            printmetric(metric_prefix + "co_status", ts, status_map[device.co_status], tags)
            printmetric(metric_prefix + "smoke_status", ts, status_map[device.smoke_status], tags)

def printmetric(metric, ts, value, tags):
  # Warning, this should be called inside a lock
  if tags:
    tags = " " + " ".join("%s=%s" % (tidy_string(name), tidy_string(value))
                          for name, value in tags.iteritems())
  else:
    tags = ""
  print ("%s %d %s %s"
         % (ROOT_METRIC + "." + metric, ts, value, tags))

def tidy_string(str):
    return str.replace(" ","").replace("&", "And")

def main():
    config = get_config()
    if config != None:
        collection_interval = config['collection_interval']
        client_id = config['client_id']
        client_secret = config['client_secret']
        access_token_cache_file = '/opt/nest.json'

        napi = nest.Nest(client_id=client_id, client_secret=client_secret, access_token_cache_file=access_token_cache_file)

        if napi.authorization_required:
            #utils.err("Nest Authorization Required")
            print ('Nest Authorization Required')

        collect_all_devices(napi)

        time.sleep(collection_interval)
    else:
        time.sleep(60)

if __name__ == "__main__":
    sys.exit(main())
