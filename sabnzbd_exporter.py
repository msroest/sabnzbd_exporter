#!/usr/bin/env python3

import os
import sys
import requests
import threading
import logging
import time
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY


logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,  datefmt='%Y/%m/%d %H:%M:%S')

METRICS_PORT = int(os.getenv('METRICS_PORT', 9387))
METRICS_ADDR = os.getenv('METRICS_ADDR', '0.0.0.0')
APIBASEURLS = os.getenv('SABNZBD_BASEURLS',os.getenv('SABNZBD_BASEURL','')).split(',')
APIKEYS = os.getenv('SABNZBD_APIKEYS', os.getenv('SABNZBD_APIKEY','')).split(',')

if APIBASEURLS == ['']: 
    logging.error("Either SABNZBD_BASEURL or SABNZBD_BASEURLS environment variable is required")
    sys.exit(1)
if APIKEYS == ['']:
    logging.error('Either SABNZBD_APIKEY or SABNZBD_APIKEY environment variable is required')
    sys.exit(1)
if len(APIBASEURLS) != len(APIKEYS):
    logging.error(f'Number of API urls {len(APIBASEURLS)} doesn\'t match number of API keys {len(APIKEYS)}')
    sys.exit(1)

logging.info("Starting sabnzbd_exporter on port: %d", METRICS_PORT)
logging.info("Connecting to %s", str(APIBASEURLS))

url_to_key_map={}
for i in range(len(APIBASEURLS)):
    url_to_key_map[APIBASEURLS[i]] = APIKEYS[i]

def getAPIUrl(base_url, mode):
    return '{}/api?output=json&apikey={}&mode={}'.format(base_url, url_to_key_map[base_url], mode)

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


class CustomCollector(object):
    def collect(self):
        try:
            for base_url in APIBASEURLS:
                server_stats_url = getAPIUrl(base_url,'server_stats')
                start = time.time()
                server_stats = requests.get(server_stats_url).json()
                elapsed = time.time() - start
                logging.info("Request to %s returned in %s",
                            server_stats_url, elapsed)
                dwn = GaugeMetricFamily(
                    'sabnzbd_download_bytes', 'SABnzbd Overall download metrics', labels=['period', 'sabnzbd_instance'])
                dwn.add_metric(['total', base_url], server_stats['total'])
                dwn.add_metric(['day', base_url], server_stats['day'])
                dwn.add_metric(['week', base_url], server_stats['week'])
                dwn.add_metric(['month', base_url], server_stats['month'])
                yield dwn
                server_dwn = GaugeMetricFamily('sabnzbd_server_download_bytes', 'SABnzbd per server download metrics', labels=[
                                            'server', 'period', 'sabnzbd_instance'])
                for server, metrics in server_stats['servers'].items():
                    for metric, val in metrics.items():
                        if metric != 'daily' and metric != 'articles_tried' and metric != 'articles_success':
                            server_dwn.add_metric(
                                [server, metric, base_url], val)
                yield server_dwn
                start = time.time()
                queue_stats_url = getAPIUrl(base_url,'queue')
                queue_stats = requests.get(queue_stats_url).json()["queue"]
                elapsed = time.time() - start
                logging.info("Request to %s returned in %s",
                            queue_stats_url, elapsed)
                qsize = GaugeMetricFamily(
                    'sabnzbd_queue_size', 'SABnzbd Current Queue Length', labels=['sabnzbd_instance'])
                qsize.add_metric([base_url], queue_stats['noofslots_total'])
                yield qsize
                drate = GaugeMetricFamily(
                    'sabnzbd_queue_download_rate_bytes_per_second', 'SABnzbd download rate', labels=['sabnzbd_instance'])
                drate.add_metric([base_url], float(queue_stats['kbpersec'])*1024)
                yield drate
                qremaining_bytes = GaugeMetricFamily(
                    'sabnzbd_queue_remaining_bytes', 'SABnzbd queue remaining size', labels=['sabnzbd_instance'])
                qremaining_bytes.add_metric(
                    [base_url], float(queue_stats['mbleft'])*1024*1024)
                yield qremaining_bytes
                qtotal_bytes = GaugeMetricFamily(
                    'sabnzbd_queue_total_size_bytes', 'SABnzbd queue total size', labels=['sabnzbd_instance'])
                qtotal_bytes.add_metric(
                    [base_url], float(queue_stats['mb'])*1024*1024)
                yield qtotal_bytes
                qremaining_time = GaugeMetricFamily(
                    'sabnzbd_queue_remaining_seconds', 'SABnzbd estimated time remaining', labels=['sabnzbd_instance'])
                qremaining_time.add_metric(
                    [base_url], get_sec(queue_stats['timeleft']))
                yield qremaining_time
        except Exception as inst:
            logging.error('Error getting stats: %s', inst)


REGISTRY.register(CustomCollector())
start_http_server(port=METRICS_PORT, addr=METRICS_ADDR)

DE = threading.Event()
DE.wait()
