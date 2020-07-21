FROM python:3.8.3-alpine3.11

WORKDIR /opt/resource/

COPY check.py /opt/resource/check
COPY in.py /opt/resource/in
COPY out.py /opt/resource/out

RUN pip3 install requests python-dateutil
RUN chmod +x /opt/resource/check /opt/resource/in /opt/resource/in
