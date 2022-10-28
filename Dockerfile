FROM python:3.10-slim
# TODO Изменить докерфайл перед финалом, чтобы он не копировал все файлы
ENV PYTHONUNBUFFERED 1
WORKDIR /calendar
ADD . /calendar
#COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#COPY manage.py .
#COPY .env .
#COPY todolist todolist
#COPY core core

CMD python manage.py runserver --noreload 0.0.0.0:8000
