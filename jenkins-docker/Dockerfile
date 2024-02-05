FROM ubuntu:jammy

WORKDIR /

COPY integration-test.sh /integration-test.sh
RUN cat integration-test.sh
RUN apt-get update && apt-get install --yes curl

CMD sh /integration-test.sh