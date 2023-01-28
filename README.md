This is testd on Raspberry Pi 4 4GB with 32bit OS.

Based on ZachGoldberg/nest-graph, fixed Dockerfile/tCollector to explicitly use python2. Also change arch to armv7. 

# History

Based on jeff89179's work, which is based on peterot's work (peterot/nest-graph). Updated for the new Google version of the nest device APIs.

Based on Axlan's updated python-next which uses said Google APIs. Pleaes read the README there https://github.com/axlan/python-nest to learn how to
authenticate with the API, it's nuanced and requires following the instructions carefully.

# Nest Metrics Collector

This project is a slightly over engineered solution for collecting metrics from [Nest](https://nest.com) devices (i.e. temperature, humidity, alarm state etc.) such that they can be visualised in a customisable way.

The stack relies on [OpenTSDB](http://opentsdb.net) for the metrics storage and [Grafana](https://grafana.com/grafana) for the visualisation. The metrics collection is provided by a custom Python collector which runs within the [OpenTSDB tCollector](http://opentsdb.net/docs/build/html/user_guide/utilities/tcollector.html) service.

Everything is packaged in a self-contained Docker container allowing it to be deployed anywhere.

![Grafana dashboard screen shot](https://github.com/peterot/nest-graph/blob/master/images/ScreenShot.png?raw=true "Screen Shot")

# Deployment Steps

1. Install Docker.
2. Follow the [readme steps](https://github.com/axlan/python-nest) at axlan/python-nest to generate a project_id, client_id and client_secret
3. Pull and run the Docker container.
4. Run a config script on the Docker container to provide three credentials.
5. Visit the [Grafana web console](localhost:3000) and start playing with all the graphs. (data takes 1-2 minutes to start)

## Install Docker

Follow the [platform specific install instructions](https://docs.docker.com/engine/installation/).

## Docker Deployment

First build the docker image:

```commandline
docker build . -t nest-graph
```

Make a folder on the host machine to store data and auth access credentials
```
mkdir -p /opt/nestdata
```

Start the container running with the ports for [Grafana](https://grafana.com/grafana) (3000) and [OpenTSDB](http://opentsdb.net) (4242) mapped to localhost:

```commandline
docker run -d -p 4242:4242 -p 3000:3000 --restart unless-stopped -v /opt/nestdata:/data nest-graph
```
The previous command will return the container id as a long string. Copy this for use in the next step.

## Configure Credentials

It is necessary to execute a small python script on the docker container to setup the Nest API credentials. The stript will ask for the id and secret obtained when the developer account was set up. It will then output a URL which you must visit to inform Nest that you are happy to allow the metrics collector the specified access. Once accepted it will give you a pin which must be provided to the config script.

```commandline
docker exec -it [CONTAINER-ID] /usr/bin/python3 /opt/nest-auth.py
```

## Grafana

[Grafana](https://grafana.com/grafana) will already have been configured with the [OpenTSDB](http://opentsdb.net) datasource and two example dashboards.

* Thermostats Overview - graphs showing all metrics from all the associated Nest thermostats.
* Smoke/CO Alarms - graphs showing the alarm state for all the associated Nest smoke/co alarms

You can access [Grafana](https://grafana.com/grafana) at <localhost:3000> with default credentials `admin:admin`.

## OpenTSDB

If you wish to play with OpenTSDB directly you can access the web console on <localhost:4242>

## Stored Metrics

* `nest.away`
* `nest.num_thermostats` - away state; 'home': 1, 'away': 0, 'unknown': -1
* `nest.thermostat.temperature`
* `nest.thermostat.humidity`
* `nest.thermostat.target` - target temperature
* `nest.thermostat.eco.temperature.low`
* `nest.thermostat.eco.temperature.high`
* `nest.thermostat.hvac_state` - heating state; 'heating': 1, 'off': 0, 'cooling': -1
* `nest.thermostat.is_online` - online state; 'online': 1, 'offline': 0
* `nest.smoke_co_alarm.co_status` - 'ok': 0, 'warning': 1, 'emergency': 2
* `nest.smoke_co_alarm.smoke_status` - 'ok': 0, 'warning': 1, 'emergency': 2

# Acknowledgements

In addition to [Grafana](https://grafana.com/grafana) and [OpenTSDB](http://opentsdb.net) this project relies on the excellent Python client for accessing the Nest API [python-google-nest](https://github.com/axlan/python-nest).
