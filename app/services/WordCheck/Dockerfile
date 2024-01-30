FROM python:alpine3.19
# FROM python:3.10.12

WORKDIR /wordle

COPY requirements.txt /wordle/requirements.txt

RUN python3 -m pip install --no-cache-dir --upgrade -r /wordle/requirements.txt

COPY ./ /wordle/app/services/WordCheck

CMD ["uvicorn", "app.services.WordCheck.WordCheck:app", "--host", "0.0.0.0", "--port", "9100"]