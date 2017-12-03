# sabnzbd_exporter

This is a metrics exporter for sending statistics from sabnzbd (https://sabnzbd.org/) to prometheus (http://prometheus.io) 

## Requirements
* python3
* prometheus_client (https://github.com/prometheus/client_python)
* requests (http://docs.python-requests.org/en/latest/#)
OR
docker run -E "SABNZBD_HOST=<IP>" -E "SABNZBD_PORT=8080" -E "SABNZBD_APIKEY=<apikey>" -p 9199:9199 msroest/sabnzbd_exporter
