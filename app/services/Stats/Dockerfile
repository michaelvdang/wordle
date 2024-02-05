FROM python:alpine3.19
# FROM python:3.10.12

WORKDIR /wordle

RUN ls
COPY requirements.txt /wordle/requirements.txt
# COPY ./.env /wordle/.env

# RUN python3 -m pip install --no-cache-dir --upgrade -r /wordle/requirements.txt
RUN python3 -m pip install --upgrade -r /wordle/requirements.txt

COPY ./ /wordle/app/services/Stats

# ## include these lines if the service needs these databases (stats, check, validation)
# ## but these lines create different databases for each container (not shared)
# RUN mkdir -p /wordle/var
# RUN ./bin/init-docker.sh

CMD ["uvicorn", "app.services.Stats.UserStatsRedis:app", "--host", "0.0.0.0", "--port", "9000"]