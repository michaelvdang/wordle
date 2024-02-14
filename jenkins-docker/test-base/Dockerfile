FROM nginx:alpine

WORKDIR /

# RUN apt-get update && apt-get install --yes curl

COPY test.sh /test.sh

CMD sh test.sh && cat output.txt