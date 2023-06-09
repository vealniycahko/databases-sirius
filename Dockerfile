FROM python:3.9.14

WORKDIR /flask_app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY main.py .
COPY des_companies.py .
COPY migrations/ ./migrations/
COPY static/ ./static/

ENV FLASK_APP main.py
