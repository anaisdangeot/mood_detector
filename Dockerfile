FROM python:3.10.6-buster

COPY code_mood /code_mood
COPY requirements_prod.txt /requirements_prod.txt

RUN pip install --upgrade pip
RUN pip install -r requirements_prod.txt

CMD uvicorn code_mood.api.fast:app --host 0.0.0.0 --port $PORT
