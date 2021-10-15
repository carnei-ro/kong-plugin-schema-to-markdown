FROM python:3.7-alpine3.13 AS compiled_image
# hadolint ignore=DL3013
RUN apk add --no-cache build-base \
    && pip install -U setuptools pip \
    && python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONASYNCIODEBUG=1

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.7-alpine3.13

ENV APP_DIR=/app \
    APP_USER=app \
    PATH="/opt/venv/bin:$PATH"

RUN set -ex \
 && addgroup -g 673 "$APP_USER" \
 && adduser -D -u 673 -G "$APP_USER" "$APP_USER"

COPY --from=compiled_image /opt/venv /opt/venv

COPY plugin_schema_to_markdown "$APP_DIR"

WORKDIR /app

USER "$APP_USER"

ENTRYPOINT ["python", "main.py"]
