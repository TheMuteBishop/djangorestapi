FROM python:3.7-alpine
MAINTAINER TheMuteBishop

#environment valiables
ENV PYTHONUNBUFFERED 1

#copy requirments.txt from local to container
COPY ./requirments.txt /requirments.txt 

#inatall dependencies
RUN pip install -r /requirments.txt

RUN mkdir /app
WORKDIR /app

# copy local project into container /app
COPY ./src /app

#create new user & switch to user
RUN adduser -D bishop
USER bishop