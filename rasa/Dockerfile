FROM rasa/rasa:3.2.4-full

WORKDIR '/app'
COPY . /app
USER root

COPY ./data /app/data

# train a new rasa model
RUN rasa train --data data --out models

# VOLUME /app
# VOLUME /app/data
# VOLUME /app/models

# set entrypoint for interactive shells
ENTRYPOINT ["rasa"]
# command to run when container is called to run
CMD ["run", "--enable-api"]