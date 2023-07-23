FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN mkdir /Traders

WORKDIR /Traders

ADD . /Traders

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "makemigrations", "&&", "python", "manage.py", "migrate", "&&", "python", "manage.py", "runserver", "0.0.0.0:8000"]
