# sabnzbd_exporter

This is a metrics exporter for sending statistics from sabnzbd (https://sabnzbd.org/) to prometheus (http://prometheus.io).  Example scrape configurations and a grafana dashboard can be found in [Examples](examples/)

## Configuration
This exporter is configured by environment variables.  There are 2 required environment variables
  * SABNZBD_BASEURLS - Comma seperated list of sabnzbd servers to connect to in the fomat http://\<sabnzbd host/ip\>:\<port\>/sabnzbd
  * SABNZBD_APIKEYS - Comma seperated list of API keys.  Positionally each API key must be for the same server as in the equivilent position of the SABNZBD_BASEURLS

(Previously this module only supported a single server and so the environment variables were not pluralized SABNZBD_BASEURL & SABNZBD_APIKEY these values are still supported for backwards compatibility but the plural versions are preferred)

## Running/Developing
1. Create a new python virtual env `python3 -m venv .venv`
2. Install the required modules into your venv `./.venv/bin/pip3 install -r requirements.txt`
3. Start the server locally
```
SABNZBD_BASEURLS=http://<sabnzbd host/ip>:<port>/sabnzbd SABNZBD_APIKEYS=<apikey> ./.venv/bin/python3 sabnzbd_exporter.py
```

## Running using docker
```
docker run \
   -e SABNZBD_BASEURLS=http://<sabnzbd host/ip>:<port>/sabnzbd \
   -e SABNZBD_APIKEYS=<apikey> \
   -p 9387:9387 \
   -d --restart=always \
   -n sabnzbd_exporter \
   msroest/sabnzbd_exporter
```

## Exported Metrics
Common Labels
  - sabnzbd_instance

Name |  Description | Metric Type | Labels
-----|--------------|-------------|--------
sabnzbd_download_bytes | Total data download | Gauge | period
sabnzbd_server_download_bytes | Data download quantity by server | Gauge | server, period
sabnzbd_queue_size | Length of the current download queue | Gauge | 
sabnzbd_queue_download_rate_bytes_per_second | Curent download rate | Gauge | 
sabnzbd_queue_remaining_bytes | Queue bytes remaining | Gauge |
sabnzbd_queue_total_size_bytes | Queue total size bytes | Gauge |
sabnzbd_queue_remaining_seconds | Estimated queue time remaining | Gauge |
sabnzbd_paused | Is sabnzbd paused | Guage |

* Period label values (total,day,week,month)