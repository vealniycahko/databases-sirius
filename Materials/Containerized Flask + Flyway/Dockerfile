FROM python:3.9.14

WORKDIR /flask_app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY main.py .
# нужно так же скопировать deserialization.py, если он есть
# COPY deserialization.py .

ENV FLASK_APP main.py
