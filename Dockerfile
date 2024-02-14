FROM python:alpine3.19
# FROM python:3.10.12

WORKDIR /wordle

COPY orc-requirements.txt /wordle/orc-requirements.txt

RUN python3 -m pip install -r /wordle/orc-requirements.txt
# RUN python3 -m pip install --no-cache-dir --upgrade -r /requirements.txt

COPY . /wordle/

## include these lines if the service needs these databases (stats, check, validation)
RUN mkdir -p /wordle/var
RUN chmod 544 /wordle/bin/docker-init-db.sh
RUN chmod 544 /wordle/bin/TopTen.py
RUN sh /wordle/bin/docker-init-db.sh

CMD ["uvicorn", "Orchestrator:app", "--host", "0.0.0.0", "--port", "9400"]