FROM python:3

ENV DBuser = admin
ENV DBpass = password

WORKDIR /usr/src/homeApp

COPY . .

RUN apt-get update
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]