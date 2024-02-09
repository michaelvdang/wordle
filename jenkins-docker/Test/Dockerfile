FROM dwdraju/alpine-curl-jq

WORKDIR /

# RUN apt-get update && apt-get install --yes curl

# RUN apt install --yes jq

RUN pwd 

RUN ls -al

COPY curl-orc.sh /curl-orc.sh

CMD sh /curl-orc.sh && cat /data/output.txt