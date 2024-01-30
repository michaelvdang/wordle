FROM python:alpine3.19
# FROM python:3.10.12

WORKDIR /wordle

COPY requirements.txt /requirements.txt

RUN python3 -m pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./ /wordle

## include these lines if the service needs these databases (stats, check, validation)
## but these lines create different databases for each container (not shared)
RUN mkdir -p /wordle/var
RUN chmod 544 ./bin/docker-init-db.sh
RUN chmod 544 ./bin/TopTen.py
RUN ./bin/docker-init-db.sh

# multiple calls to uvicorn doesn't work
## build each image separately, uncomment each one to build, then run docker compose
# CMD ["uvicorn", "UserStatsRedis:app", "--host", "0.0.0.0", "--port", "9000"]
# CMD ["uvicorn", "WordCheck:app", "--host", "0.0.0.0", "--port", "9100"]
# CMD ["uvicorn", "WordValidation:app", "--host", "0.0.0.0", "--port", "9200"]
# CMD ["uvicorn", "Play:app", "--host", "0.0.0.0", "--port", "9300"]
CMD ["uvicorn", "Orchestrator:app", "--host", "0.0.0.0", "--port", "9400"]