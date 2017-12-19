import os
import requests
import prometheus_client
import threading
import logging
import time
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

PORT=9387

APIBASEURL = os.environ['SABNZBD_BASEURL']
APIKEY = os.environ['SABNZBD_APIKEY']

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level=logging.INFO,  datefmt='%Y/%m/%d %H:%M:%S')
logging.info("Starting sabnzbd_exporter on port: %d",PORT)
logging.info("Connecting to %s",APIBASEURL)

def getAPIUrl(mode):
    return '{}/api?output=json&apikey={}&mode={}'.format(APIBASEURL, APIKEY, mode)

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

class CustomCollector(object):
    def collect(self):
        try:
            server_stats_url = getAPIUrl('server_stats')
            start = time.time()
            server_stats = requests.get(server_stats_url).json()
            elapsed = time.time() - start
            logging.info("Request to %s returned in %s",server_stats_url, elapsed)
            dwn = GaugeMetricFamily('sabnzbd_download_bytes', 'SABnzbd Overall download metrics', labels=['period'])
            dwn.add_metric(['total'], server_stats['total'])
            dwn.add_metric(['day'], server_stats['day'])
            dwn.add_metric(['week'], server_stats['week'])
            dwn.add_metric(['month'], server_stats['month'])
            yield dwn
            server_dwn = GaugeMetricFamily('sabnzbd_server_download_bytes','SABnzbd per server download metrics',labels=['server','period'])
            for server, metrics in server_stats['servers'].items():
                for metric,val in metrics.items():
                    server_dwn.add_metric([server,metric],val)
            yield server_dwn
            start = time.time()
            queue_stats_url = getAPIUrl('queue')
            queue_stats = requests.get(queue_stats_url).json()["queue"]
            elapsed = time.time() - start
            logging.info("Request to %s returned in %s",queue_stats_url, elapsed)
            yield GaugeMetricFamily('sabnzbd_queue_size','SABnzbd Current Queue Length',value=queue_stats['noofslots_total'])
            yield GaugeMetricFamily('sabnzbd_queue_download_rate_bytes_per_second','SABnzbd download rate',value=float(queue_stats['kbpersec'])*1024)
            yield GaugeMetricFamily('sabnzbd_queue_remaining_bytes','SABnzbd queue remaining size',value=float(queue_stats['mbleft'])*1024*1024)
            yield GaugeMetricFamily('sabnzbd_queue_total_size_bytes','SABnzbd queue total size',value=float(queue_stats['mb'])*1024*1024)
            yield GaugeMetricFamily('sabnzbd_queue_remaining_seconds','SABnzbd estimated time remaining',value=get_sec(queue_stats['timeleft']))
        except Exception as inst:
            logging.error('Error getting stats: %s', inst)


REGISTRY.register(CustomCollector())
start_http_server(PORT)

DE = threading.Event()
DE.wait()
