FROM ubuntu:jammy

WORKDIR /

COPY integration-test.sh /integration-test.sh
RUN cat integration-test.sh
RUN apt-get update && apt-get install --yes curl

RUN sh /integration-test.sh
RUN cat google.txt
RUN cat orc.txt

CMD sh /integration-test.sh