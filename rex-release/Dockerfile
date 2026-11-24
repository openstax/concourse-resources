# The latest image is from 2019, so we don't expect it to be updated anymore. It's pinned now to pin the Python and botocore that redirects.py uses (Python 3.8, botocore 1.12)
FROM garland/aws-cli-docker@sha256:9679450d3b1d65b61deb315ad67c9820db2c291407e97c277be23752f7856420

RUN apk --no-cache update && \
  apk --no-cache add jq bash && \
  rm -rf /var/cache/apk/*

WORKDIR /opt/resource/

COPY check.sh /opt/resource/check
COPY in.sh /opt/resource/in
COPY out.sh /opt/resource/out
COPY redirects.py /opt/resource/redirects.py

RUN chmod +x /opt/resource/check /opt/resource/in /opt/resource/in
