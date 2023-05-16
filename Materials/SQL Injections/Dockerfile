FROM python:3.9.14

WORKDIR /flask_app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY main.py .
COPY migrations/ ./migrations/

ENV FLASK_APP main.py
