FROM python:3.10

WORKDIR /app/

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY src/ /app/

RUN cd /app

EXPOSE 8000