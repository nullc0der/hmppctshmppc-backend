FROM python:3.7
LABEL maintainer Prasanta Kakati <prasantakakati1994@gmail.com>
RUN apt-get update && \
    apt-get install --yes build-essential postgresql-client \
    libpq-dev curl
RUN mkdir /hmppctshmppc-backend
WORKDIR /hmppctshmppc-backend
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
COPY pyproject.toml poetry.lock /hmppctshmppc-backend/
RUN . $HOME/.poetry/env && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev
COPY . /hmppctshmppc-backend
CMD [ "sh", "start.sh" ]
