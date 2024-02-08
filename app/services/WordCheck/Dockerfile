FROM python:alpine3.19
# FROM python:3.10.12

WORKDIR /wordle

COPY ./ /wordle/app/services/WordCheck
# COPY requirements.txt /wordle/requirements.txt

RUN python3 -m pip install --upgrade -r /wordle/app/services/WordCheck/requirements.txt

CMD ["uvicorn", "app.services.WordCheck.WordCheck:app", "--host", "0.0.0.0", "--port", "9100"]