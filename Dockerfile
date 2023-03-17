FROM python:3.10-slim

WORKDIR /app

RUN apt update && apt install zip unzip

ADD cat.jpeg .
ADD main.py .

ENTRYPOINT ["python3", "main.py"]