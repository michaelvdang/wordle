FROM python:3.10.12

WORKDIR /wordle

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./ /wordle

RUN ls

# CMD ["ls"]

# CMD ["pwd"]

# RUN uvicorn Play:app --host 0.0.0.0 --port 8001 
# RUN uvicorn WordCheck:app --host 0.0.0.0 --port 8002

CMD ["uvicorn", "Orchestrator:app", "--host", "0.0.0.0", "--port", "8004"]