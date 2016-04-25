FROM ubuntu:latest
MAINTAINER Xiaogang Han "xganghan@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential libxml2-dev libxslt1-dev zlib1g-dev
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
