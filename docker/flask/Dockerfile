FROM python:3.9
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip3 install pipenv
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile
COPY . .
CMD ["pipenv", "run", "server", "-h", "0.0.0.0"]
EXPOSE 5000