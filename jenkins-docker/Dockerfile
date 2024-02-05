FROM ubuntu:jammy

WORKDIR /

RUN apt-get update && apt-get install --yes curl

COPY integration-test.sh /integration-test.sh
RUN cat integration-test.sh

RUN sh /integration-test.sh
RUN cat google.txt
# RUN cat app.txt

CMD sh /integration-test.sh