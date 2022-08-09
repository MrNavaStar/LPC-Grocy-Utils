FROM python:3.10-alpine
COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT ["python3", "router.py"]