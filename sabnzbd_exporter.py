import os
import requests
import prometheus_client
import threading
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

PORT = int(os.environ['PORT'])
APIBASEURL = os.environ['SABNZBD_BASEURL']
APIKEY = os.environ['SABNZBD_APIKEY']

print("Starting sabnzbd_exporter on port: {}".format(PORT))
print("Connecting to {}".format(APIBASEURL))

def getAPIUrl(mode):
    return '{}/api?output=json&apikey={}&mode={}'.format(APIBASEURL, APIKEY, mode)

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

class CustomCollector(object):
    def collect(self):
        try:
            server_stats = requests.get(getAPIUrl('server_stats')).json()
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
            queue_stats = requests.get(getAPIUrl('queue')).json()["queue"]
            yield GaugeMetricFamily('sabnzbd_queue_size','SABnzbd Current Queue Length',value=queue_stats['noofslots_total'])
            yield GaugeMetricFamily('sabnzbd_queue_download_rate_bytes_per_second','SABnzbd download rate',value=float(queue_stats['kbpersec'])*1024)
            yield GaugeMetricFamily('sabnzbd_queue_remaining_bytes','SABnzbd queue remaining size',value=float(queue_stats['mbleft'])*1024*1024)
            yield GaugeMetricFamily('sabnzbd_queue_total_size_bytes','SABnzbd queue total size',value=float(queue_stats['mb'])*1024*1024)
            yield GaugeMetricFamily('sabnzbd_queue_remaining_seconds','SABnzbd estimated time remaining',value=get_sec(queue_stats['timeleft']))
        except Exception as inst:
            print('Error getting stats')
            print(inst)


REGISTRY.register(CustomCollector())
start_http_server(PORT)

DE = threading.Event()
DE.wait()
