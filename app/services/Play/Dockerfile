FROM python:alpine3.19

WORKDIR /wordle

COPY play-requirements.txt /wordle/app/services/Play/play-requirements.txt

RUN python3 -m pip install -r /wordle/app/services/Play/play-requirements.txt

COPY . /wordle/app/services/Play

CMD ["uvicorn", "app.services.Play.Play:app", "--host", "0.0.0.0", "--port", "9300"]