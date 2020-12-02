# sabnzbd_exporter

This is a metrics exporter for sending statistics from sabnzbd (https://sabnzbd.org/) to prometheus (http://prometheus.io) 


## Requirements
* python3
* prometheus_client (https://github.com/prometheus/client_python)
* requests (http://docs.python-requests.org/en/latest/#)

OR

docker run -e SABNZBD_BASEURL=http://\<sabnzbd host/ip\>:port/sabnzbd -e SABNZBD_APIKEY=\<apikey\> -p 9387:9387 -d --restart=always msroest/sabnzbd_exporter

