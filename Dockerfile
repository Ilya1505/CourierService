FROM python:3.11

RUN mkdir app
WORKDIR /app/


RUN apt update && apt upgrade -y

RUN apt install -y python3 python3-pip gcc musl-dev

RUN apt update

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x start.sh