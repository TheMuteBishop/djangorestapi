FROM python:3.7-alpine
MAINTAINER TheMuteBishop

#environment valiables
ENV PYTHONUNBUFFERED 1

#copy requirments.txt from local to container
COPY ./requirments.txt /requirments.txt 

#install dependencies
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .dev-dependencies \
        gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirments.txt
RUN apk del .dev-dependencies

RUN mkdir /app
WORKDIR /app

# copy local project into container /app
COPY ./src /app

#create new user & switch to user
RUN adduser -D bishop
USER bishop