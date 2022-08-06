# Splunky FastAPI app

## Overview
Main goal of this prohect is to practice good practices when creating an API.

### Tecnlogies used
1. FastAPI
2. Alembic
3. Tweepy
4. Botometer
5. Postgres

### Steps to develop with Docker
Make sure you have installed `Docker` and `docker-compose`.
1. Run `docker-compose build` to create the docker image of the app.
2. Run `docker-compose run web alembic upgrade head` to create the migrations in the Docker Postgres.
3. Run `docker-compose up` to start the three containers (App, DB and PGAdmin).
4. Start coding and enjoy!

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
Jhair Gutiérrez Solís - 2022