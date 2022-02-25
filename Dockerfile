FROM alpine:3.15

EXPOSE 9387

RUN apk add --update --no-cache python3 py3-pip curl && \
pip install prometheus_client requests

COPY sabnzbd_exporter.py /sabnzbd_exporter.py

HEALTHCHECK --interval=1m CMD /usr/bin/curl -f http://localhost:9387/ || exit 1

ENTRYPOINT ["python","/sabnzbd_exporter.py"]