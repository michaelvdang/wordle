FROM python:alpine3.19

WORKDIR /wordle

COPY wordcheck-requirements.txt /wordle/app/services/WordCheck/wordcheck-requirements.txt

RUN python3 -m pip install -r /wordle/app/services/WordCheck/wordcheck-requirements.txt

COPY . /wordle/app/services/WordCheck

CMD ["uvicorn", "app.services.WordCheck.WordCheck:app", "--host", "0.0.0.0", "--port", "9100"]