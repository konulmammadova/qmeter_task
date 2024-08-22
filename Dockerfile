FROM python:3.10.14-slim
# python version without unnecessary load

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV APP_ROOT /app

COPY . ${APP_ROOT}

WORKDIR ${APP_ROOT}

RUN pip install pip --upgrade && pip install --no-cache-di -r requirements.txt