FROM ubuntu:jammy

WORKDIR /

RUN apt-get update && apt-get install --yes curl

COPY curl-orc.sh /curl-orc.sh

CMD sh /curl-orc.sh && cat wv.txt && cat orc.txt && cat play.txt && cat wc.txt