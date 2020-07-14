FROM python:3.7.8-alpine3.12

# set work directory
WORKDIR /usr/src/tsts

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add jpeg-dev zlib-dev libjpeg
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# RUN adduser -D ruslan
# WORKDIR /home/ruslan
# COPY requirements.txt requirements.txt
# RUN python -m venv venv
# RUN venv/bin/pip install -r requirements.txt
# RUN venv/bin/pip install gunicorn
# COPY . .
# COPY boot.sh ./
# RUN chmod +x boot.sh
# RUN chown -R ruslan:ruslan ./
# USER ruslan

# EXPOSE 5000
# ENTRYPOINT ["./boot.sh"]