FROM python:3.8

WORKDIR /usr/src/django_project

ENV PYTHONDONTWRITEBYETCODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/django_project
RUN pip install -r /usr/src/django_project/requirements.txt

COPY . /usr/src/django_project

EXPOSE 8000

#CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
