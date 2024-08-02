FROM python:3.9.16-alpine3.17

WORKDIR /app

COPY . .

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi \
    && apk del .build-deps

ENTRYPOINT ["python", "create-tagged-releases.py"]

CMD ["--help"]
