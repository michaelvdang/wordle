FROM python:alpine3.19
# FROM python:3.10.12

WORKDIR /wordle

COPY ./orc-requirements.txt /wordle/orc-requirements.txt

RUN python3 -m pip install -r /wordle/orc-requirements.txt
# RUN python3 -m pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./ /wordle
# COPY app/ /wordle/app/
# COPY bin/ /wordle/bin/
# COPY share/ /wordle/share/
# COPY jenkins-docker/ /wordle/jenkins-docker/
# COPY wordle-frontend/src/ /wordle/wordle-frontend/src/

## include these lines if the service needs these databases (stats, check, validation)
## but these lines create different databases for each container (not shared)
RUN mkdir -p /wordle/var
RUN chmod 544 ./bin/docker-init-db.sh
RUN chmod 544 ./bin/TopTen.py
RUN sh ./bin/docker-init-db.sh
# RUN python3 --version

# multiple calls to uvicorn doesn't work
## build each image separately, uncomment each one to build, then run docker compose
# CMD ["uvicorn", "UserStatsRedis:app", "--host", "0.0.0.0", "--port", "9000"]
# CMD ["uvicorn", "WordCheck:app", "--host", "0.0.0.0", "--port", "9100"]
# CMD ["uvicorn", "WordValidation:app", "--host", "0.0.0.0", "--port", "9200"]
# CMD ["uvicorn", "Play:app", "--host", "0.0.0.0", "--port", "9300"]
CMD ["uvicorn", "Orchestrator:app", "--host", "0.0.0.0", "--port", "9400"]