FROM ubuntu:jammy

WORKDIR /

RUN apt-get update && apt-get install --yes curl

COPY conn-check.sh /conn-check.sh
RUN cat /conn-check.sh
CMD sh /conn-check.sh && cat /conn-status.txt

## disable cache: https://stackoverflow.com/questions/9179828/github-api-retrieve-all-commits-for-all-branches-for-a-repo
# RUN curl "https://api.github.com/repos/michaelvdang/wordle/commits?per_page=1&sha=488bb5491ccda0a6a771fa4def4bb2db731e0f8b" # latest_commit 
