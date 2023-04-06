FROM python:3.11.3-alpine
MAINTAINER iDustBin "idustbin@devops.army"

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["app.py"]
