FROM python:alpine3.18

EXPOSE 9387
COPY sabnzbd_exporter.py /sabnzbd_exporter.py
COPY requirements.txt /requirements.txt
RUN apk add --update --no-cache curl && \
pip install -r /requirements.txt && rm -rf requirements.txt

HEALTHCHECK --interval=1m CMD /usr/bin/curl -f -s http://localhost:$${METRICS_PORT:-9387}/ || exit 1

ENTRYPOINT ["python","/sabnzbd_exporter.py"]
