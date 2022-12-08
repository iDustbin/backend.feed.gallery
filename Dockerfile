FROM python:3.11-alpine
MAINTAINER iDustBin "idustbin@devops.army"

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["app.py"]