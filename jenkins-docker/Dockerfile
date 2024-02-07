FROM ubuntu:jammy

WORKDIR /

RUN apt-get update && apt-get install --yes curl

# COPY integration-test.sh /integration-test.sh
# RUN cat integration-test.sh
# RUN sh /integration-test.sh

COPY curl-all.sh /curl-all.sh
RUN cat /curl-all.sh
CMD sh /curl-all.sh

# COPY ping-all.sh /ping-all.sh
# RUN cat /ping-all.sh
# CMD sh /ping-all.sh

## disable cache: https://stackoverflow.com/questions/9179828/github-api-retrieve-all-commits-for-all-branches-for-a-repo
# RUN curl "https://api.github.com/repos/michaelvdang/wordle/commits?per_page=1&sha=488bb5491ccda0a6a771fa4def4bb2db731e0f8b" # latest_commit 


# CMD sh curl-all.sh