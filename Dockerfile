FROM python:3.12

RUN set -ex && mkdir /app
WORKDIR /app


COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

CMD python manage.py migrate && gunicorn --timeout 120 -w 3 -b 0.0.0.0:80 socialnet.wsgi