# FROM dwdraju/alpine-curl-jq
FROM nginx

WORKDIR /

RUN apt-get update && apt-get install --yes curl

RUN apt update && apt install --yes jq

# COPY random-string.sh /random-string.sh

# COPY test-orc.sh /test-orc.sh

COPY ./ /

CMD bash /test-orc.sh && bash /test-stats.sh