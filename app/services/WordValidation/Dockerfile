FROM python:alpine3.19

WORKDIR /wordle

COPY wordvalidation-requirements.txt /wordle/app/services/WordValidation/wordvalidation-requirements.txt

RUN python3 -m pip install -r /wordle/app/services/WordValidation/wordvalidation-requirements.txt

COPY . /wordle/app/services/WordValidation

CMD ["uvicorn", "app.services.WordValidation.WordValidation:app", "--host", "0.0.0.0", "--port", "9200"]
