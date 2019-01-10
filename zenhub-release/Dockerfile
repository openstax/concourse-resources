FROM node:10-alpine

WORKDIR /opt/resource/

COPY check.js /opt/resource/check
COPY in.js /opt/resource/in
COPY out.js /opt/resource/out

RUN chmod +x /opt/resource/check /opt/resource/in /opt/resource/in

COPY package.json ./package.json
COPY yarn.lock ./yarn.lock
RUN yarn install
