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

# CMD ["uvicorn", "Play:app", "--host", "0.0.0.0", "--port", "8001"]
# multiple calls to uvicorn doesn't work
# CMD ["uvicorn", "WordCheck:app", "--host", "0.0.0.0", "--port", "8002"]
# CMD ["uvicorn", "UserStatsRedis:app", "--host", "0.0.0.0", "--port", "9000"]
# CMD ["uvicorn", "WordCheck:app", "--host", "0.0.0.0", "--port", "9100"]
# CMD ["uvicorn", "WordValidation:app", "--host", "0.0.0.0", "--port", "9200"]
CMD ["uvicorn", "Play:app", "--host", "0.0.0.0", "--port", "9300"]
# CMD ["uvicorn", "Orchestrator:app", "--host", "0.0.0.0", "--port", "9400"]