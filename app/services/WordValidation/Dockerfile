FROM python:alpine3.19
# FROM python:3.10.12

WORKDIR /wordle

COPY ./requirements.txt /wordle/app/services/WordValidation/requirements.txt

RUN python3 -m pip install -r /wordle/app/services/WordValidation/requirements.txt

COPY ./ /wordle/app/services/WordValidation

CMD ["uvicorn", "app.services.WordValidation.WordValidation:app", "--host", "0.0.0.0", "--port", "9200"]