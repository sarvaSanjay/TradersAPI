FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN mkdir /Traders

WORKDIR /Traders

ADD . /Traders

RUN pip install -r requirements.txt

RUN python manage.py makemigrations

RUN python manage.py migrate

EXPOSE 8000

VOLUME .:/Traders

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
