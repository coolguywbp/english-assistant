FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /backend
COPY ./app ./app 
COPY ./requirements.txt /backend/requirements.txt 
COPY ./manage.py /backend/manage.py 
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt 