FROM alpine

RUN apk --no-cache update && \
  apk --no-cache add jq bash curl && \
  rm -rf /var/cache/apk/*

WORKDIR /opt/resource/

COPY check.sh /opt/resource/check
COPY in.sh /opt/resource/in
COPY out.sh /opt/resource/out

RUN chmod +x /opt/resource/check /opt/resource/in /opt/resource/in
