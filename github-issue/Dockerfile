FROM python:3.8.3-alpine3.11

WORKDIR /opt/resource/

RUN pip3 install requests python-dateutil

COPY check.py /opt/resource/check
COPY in.py /opt/resource/in
COPY out.py /opt/resource/out

RUN chmod +x /opt/resource/check /opt/resource/in /opt/resource/in
