FROM python:alpine3.19

WORKDIR /wordle

COPY stats-requirements.txt /wordle/app/services/Stats/stats-requirements.txt

RUN python3 -m pip install -r /wordle/app/services/Stats/stats-requirements.txt

COPY . /wordle/app/services/Stats

CMD ["uvicorn", "app.services.Stats.Stats:app", "--host", "0.0.0.0", "--port", "9000"]