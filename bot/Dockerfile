FROM nikolaik/python-nodejs:latest
# FROM python:3.9 
WORKDIR /bot
COPY ./tgbot/ ./tgbot/
COPY ./requirements.txt requirements.txt 
COPY ./bot.py bot.py
RUN pip install --no-cache-dir --upgrade -r /bot/requirements.txt

# Для перезагрузки после внесения изменений приходится вот такое делать
# На проде убрать!
RUN npm install -g nodemon

CMD ["nodemon", "bot.py", "docker"]