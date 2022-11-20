#!/usr/bin/python3

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
                'project_id': nest_conf['project_id'],
                'client_secret': nest_conf['client_secret'],
                'access_token_cache_file': nest_conf['access_token_cache_file']
            }

            return config
    else:
        return None

def temperatureUnits(traits, value):
    # by default everything from google is celcius,
    if traits['Settings']['temperatureScale'] == 'CELSIUS':
        return value

    return round((value * 1.8) + 32)

def collect_all_devices(napi):
    devices = napi.get_devices()
    printmetric("num_thermostats", time.time(), len(devices), {})
    for device in devices:
        ts = time.time()
        tags = {"device":device.name}

        # Seems new google API doesn't give us structure info
        # away_val = {
        #     'home': 1,
        #     'away': 0,
        #     'unknown': -1,
        # }[structure.away]
        printmetric("away", ts, -1, tags)

        if device.type == 'THERMOSTAT':
            shortname = device.name[-7:-1]
            tags = {"structure":device.where, "device": "%s-%s" %(device.where, shortname)}
            metric_prefix = "thermostat."
            traits = device.traits
            printmetric(metric_prefix + "temperature", ts, temperatureUnits(traits, traits['Temperature']['ambientTemperatureCelsius']), tags)
            printmetric(metric_prefix + "humidity", ts, device.traits['Humidity']['ambientHumidityPercent'], tags)
            printmetric(metric_prefix + "target", ts, temperatureUnits(traits, list(device.traits['ThermostatTemperatureSetpoint'].values())[0]), tags)
            printmetric(metric_prefix + "eco.temperature.low", ts, temperatureUnits(traits, device.traits['ThermostatEco']['heatCelsius']), tags)
            printmetric(metric_prefix + "eco.temperature.high", ts, temperatureUnits(traits, device.traits['ThermostatEco']['coolCelsius']), tags)

            online_val = {
                True: 1,
                False: 0
            }[traits['Connectivity']['status'] == "ONLINE"]
            printmetric(metric_prefix + "is_online", ts, online_val, tags)

            hvac_state_val = {
                'HEATING': 1,
                'OFF': 0,
                'COOLING': -1,
            }[traits['ThermostatHvac']['status']]
            printmetric(metric_prefix + "hvac_state", ts, hvac_state_val, tags)

        # for device in structure.smoke_co_alarms:
        #     tags = {"structure":structure.name, "device":device.name}
        #     metric_prefix = "smoke_co_alarm."

        #     status_map = {
        #         'ok': 0,
        #         'warning': 1,
        #         'emergency': 2
        #     }
        #     printmetric(metric_prefix + "co_status", ts, status_map[device.co_status], tags)
        #     printmetric(metric_prefix + "smoke_status", ts, status_map[device.smoke_status], tags)

def printmetric(metric, ts, value, tags):
  # Warning, this should be called inside a lock
  if tags:
    tags = " " + " ".join("%s=%s" % (tidy_string(name), tidy_string(value))
                          for name, value in tags.items())
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
        project_id = config['project_id']
        client_secret = config['client_secret']
        access_token_cache_file = '/opt/nest.json'

        napi = nest.Nest(client_id=client_id, project_id=project_id, client_secret=client_secret, access_token_cache_file=access_token_cache_file)


        collect_all_devices(napi)

        time.sleep(collection_interval)
    else:
        print("Unable to find nest api auth config, looping...")
        time.sleep(60)

if __name__ == "__main__":
    sys.exit(main())
