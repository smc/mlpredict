# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7-buster

MAINTAINER Santhosh Thottingal "santhosh.thottingal@gmail.coom"

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip3 install -r requirements.txt
RUN apt-get update
RUN apt-get install curl -y
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && apt-get install nodejs -y
RUN npm install
RUN npm run build
ENV NAME mlpredict

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 mlpredictweb:app
