FROM frolvlad/alpine-python3:latest

ENV PORT=9199

EXPOSE 9199

RUN pip install prometheus_client requests

COPY sabnzbd_exporter.py /sabnzbd_exporter.py

ENTRYPOINT ["python","/sabnzbd_exporter.py"]