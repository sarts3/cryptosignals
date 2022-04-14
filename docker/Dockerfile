FROM python:3.9-alpine

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/

RUN set -ex \
  && apk update \
  && apk add --no-cache linux-headers sudo curl git gcc musl-dev \
  && pip install -r /code/requirements.txt \
  && apk --purge del postgresql-dev musl-dev\
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /root/.cache

ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING=utf-8

ADD cryptosignals/ /code/cryptosignals/
ADD price/ /code/price/
ADD fixtures/ /code/fixtures/
ADD scripts/ /code/scripts/
ADD manage.py /code/
ADD docker/run.sh /run.sh
RUN chmod +x /run.sh

RUN echo "* * * * * curl localhost:8000/prices/new_batch >> /code/batch.log" >> /etc/crontabs/root
CMD python3 manage.py runserver 0.0.0.0:8000
