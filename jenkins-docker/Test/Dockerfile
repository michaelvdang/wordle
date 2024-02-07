FROM ubuntu:jammy

WORKDIR /

RUN apt-get update && apt-get install --yes curl

COPY curl-orc.sh /curl-orc.sh

CMD sh curl-orc.sh && cat /first_curl.txt