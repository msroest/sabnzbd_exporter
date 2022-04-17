# sabnzbd_exporter

This is a metrics exporter for sending statistics from sabnzbd (https://sabnzbd.org/) to prometheus (http://prometheus.io) 

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

## Prometheus Scrape Configuration
```
- job_name: sabnzbd-exporter
  honor_timestamps: true
  scrape_interval: 5s
  scrape_timeout: 5s
  metrics_path: /metrics
  scheme: http
  follow_redirects: true
  static_configs:
  - targets:
    - <exporter machine name/ip>:9387
```