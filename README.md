# Nest Metrics Collector

This project is a slightly over engineered solution for collecting metrics from Nest devices (i.e. temperature, humidity, alarm state etc.) such that they can be visualised in a customisable way.

The stack relies on OpenTSDB for the metrics storage and Grafana for the visualisation. The metrics collection is provided by a custom Python collector which runs within the OpenTSDB tCollector service.

Everything is packaged in a self-contained Docker container allowing it to be deployed anywhere. 

# Deployment Steps

1. Install Docker.
2. Set up a Nest developer account to allow API access to the devices in your account
3. Pull and run the Docker container.
4. Run a config script on the Docker container to provide Nest API credentials.
5. Visit the Grafana web console and start playing with all the graphs.

## Install Docker

Follow the platform specific install instructions.

# Nest Developer Account

You will need a Nest developer account, and a Product on the Nest developer portal:

1. Visit `Nest Developers <https://developers.nest.com/>`_, and sign in. Create an account if you don't have one already.

2. Fill in the account details:

  - The "Company Information" can be anything.

3. Submit changes.

4. Click "`Products <https://developers.nest.com/products>`_" at top of page.

5. Click "`Create New Product <https://developers.nest.com/products/new>`_"

6. Fill in details:

  - Product name must be unique.

  - The description, users, urls can all be anything you want.

7. For permissions, check every box it should only be necessary to request read access.

  - The description requires a specific format to be accepted.

8. Click "Create Product".

9. Once the new product page opens the "Product ID" and "Product Secret" are located on the right side. These will be used as client_id and client_secret below.

## Docker Deployment 

First pull the docker image:

```commandline
docker pull peterot/nest-graph
```
Start the container running with the ports for Grafana (3000) and OpenTSDB (4242) mapped to localhost:

```commandline
docker run -d -p 4242:4242 -p 3000:3000 --restart unless-stopped peterot/nest-graph
```
The previous command will return the container id as a long string. Copy this for use in the next step.

## Configure Credentials

It is necessary to execute a small python script on the docker container to setup the Nest API credentials. The stript will ask for the id and secret obtained when the developer account was set up. It will then output a URL which you must visit to inform Nest that you are happy to allow the metrics collector the specified access. Once accepted it will give you a pin which must be provided to the config script.

```commandline
docker exec -it [CONTAINER-ID] /usr/bin/python /opt/nest-auth.py
```

## Grafana

Grafana will already have been configured with the OpenTSDB datasource and two example dashboards.

* Thermostats Overview - graphs showing all metrics from all the associated Nest thermostats.
* Smoke/CO Alarms - graphs showing the alarm state for all the associated Nest smoke/co alarms

You can access Grafana at localhost:3000 with default credentials `admin:admin`.

## Stored Metrics

* `nest.num_thermostats`
* `nest.thermostat.temperature`
* `nest.thermostat.humidity`
* `nest.thermostat.target` - target temperature
* `nest.thermostat.eco.temperature.low`
* `nest.thermostat.eco.temperature.high`
* `nest.thermostat.hvac_state` - heating state; 'heating': 1, 'off': 0, 'cooling': -1
* `nest.smoke_co_alarm.co_status` - 'ok': 0, 'warning': 1, 'emergency': 2
* `nest.smoke_co_alarm.smoke_status` - 'ok': 0, 'warning': 1, 'emergency': 2