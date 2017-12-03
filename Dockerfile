FROM frolvlad/alpine-python3:latest

ENV PORT=9387

EXPOSE 9387

RUN pip install prometheus_client requests

COPY sabnzbd_exporter.py /sabnzbd_exporter.py

ENTRYPOINT ["python","/sabnzbd_exporter.py"]