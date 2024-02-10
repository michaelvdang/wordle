FROM dwdraju/alpine-curl-jq

WORKDIR /

# RUN apt-get update && apt-get install --yes curl

# RUN apt install --yes jq

COPY random-string.sh /random-string.sh

COPY test-orc.sh /test-orc.sh

CMD sh /test-orc.sh && cat /data/output.txt && sh /test-stats.sh && cat /data/stats-output.txt