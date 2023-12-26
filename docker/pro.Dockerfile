# This docker file is used for local development via docker-compose
# Creating image based on official python3 image

FROM python:3.11.6-alpine3.18
LABEL maintainer="FAroogh"

# Fix python printing
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Get the django project into the docker container
COPY ./requirements /tmp/requirements
COPY ./scripts /scripts
COPY ./src /src

WORKDIR /src

EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    \
    apk add --update --no-cache postgresql-client && \
    apk add --update  postgresql-client build-base postgresql-dev \
        musl-dev linux-headers libffi-dev libxslt-dev libxml2-dev && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers libffi-dev \
        libjpeg zlib-dev jpeg-dev gcc musl-dev libxslt libxml2 &&\
    \
    /py/bin/pip install -r /temp/requirements/dev_requirements.txt && \
    \
    rm -rf /tmp && \
    \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

CMD ["web_entrypoint.sh"]
