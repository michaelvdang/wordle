FROM python:alpine3.19
# FROM python:3.10.12

WORKDIR /wordle

COPY ./ /wordle/app/services/Play
# COPY requirements.txt /wordle/requirements.txt

RUN python3 -m pip install -r /wordle/app/services/Play/requirements.txt

CMD ["uvicorn", "app.services.Play.Play:app", "--host", "0.0.0.0", "--port", "9300"]