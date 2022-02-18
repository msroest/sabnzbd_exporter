FROM python:3-alpine

EXPOSE 9387

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt && apk add curl --no-cache && rm /requirements.txt

COPY sabnzbd_exporter.py /sabnzbd_exporter.py

HEALTHCHECK --interval=1m CMD /usr/bin/curl -f http://localhost:9387/ || exit 1

ENTRYPOINT ["python","/sabnzbd_exporter.py"]