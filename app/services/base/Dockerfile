FROM python:alpine3.19

WORKDIR /

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app/main.py /app/main.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
# CMD uvicorn app.main:app --port 3000 --host 0.0.0.0