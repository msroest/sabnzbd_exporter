FROM frolvlad/alpine-python3:latest

EXPOSE 9387

RUN pip install prometheus_client requests && apk update && apk add curl

COPY sabnzbd_exporter.py /sabnzbd_exporter.py

HEALTHCHECK --interval=1m CMD /usr/bin/curl -f http://localhost:9387/ || exit 1

ENTRYPOINT ["python","/sabnzbd_exporter.py"]