FROM python:3.9
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip3 install pipenv
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock docker/flask/docker-entrypoint.sh ./
RUN pipenv install --system --deploy --ignore-pipfile
COPY . /usr/src/app/
RUN ["chmod", "+x", "/usr/src/app/docker-entrypoint.sh"]
ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]

