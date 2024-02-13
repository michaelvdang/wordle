FROM python:alpine3.19
# FROM python:3.10.12

WORKDIR /wordle

RUN ls
COPY ./ /wordle/app/services/Stats

# RUN python3 -m pip install --no-cache-dir --upgrade -r /wordle/requirements.txt
RUN python3 -m pip install -r /wordle/app/services/Stats/requirements.txt

# ## include these lines if the service needs these databases (stats, check, validation)
# ## but these lines create different databases for each container (not shared)
# RUN mkdir -p /wordle/var
# RUN ./bin/init-docker.sh

CMD ["uvicorn", "app.services.Stats.Stats:app", "--host", "0.0.0.0", "--port", "9000"]