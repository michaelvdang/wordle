FROM ubuntu:jammy

WORKDIR /

RUN apt-get update && apt-get install --yes curl

RUN apt install --yes jq

COPY curl-orc.sh /curl-orc.sh

CMD sh /curl-orc.sh && cat output.txt