# Splunky FastAPI app

## Overview
Main goal of this project is to practice good practices when creating an API.

### Tecnlogies used
1. FastAPI
2. Alembic
3. Tweepy
4. Botometer
5. Postgres

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Install and setup

### Prerequisites

#### Install python 3.10 on Linux

First, we need to add the repository and install python:

```
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10 python3.10-dev python3.10-distutils
```

Then, we need to install the version of pip for it.

```
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
```

Finally, update pip and dependencies.

```
python3.10 -m pip install --upgrade pip
python3.10 -m pip install --upgrade wheel
python3.10 -m pip install --upgrade setuptools
```

### Postgres prerequisites

This project makes use of PostgreSQL, so you will need to have it installed. In Linux based systems, the following dependencies also have to be installed.

```
sudo apt install python3-psycopg2 libssl-dev python3-dev libpq-dev
```

Then, create an environment and run from the project's main folder:

```
pip install -r requirements.txt
```

## License
Jhair Gutiérrez Solís - 2022