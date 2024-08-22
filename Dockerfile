FROM python:3.10.14-slim
# python version without unnecessary load

# Define environment variables
# Set environment variables to ensure the Python output 
# is sent straight to the terminal (without buffering) and to prevent .pyc files from being written to disk

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV APP_ROOT /app

COPY . ${APP_ROOT}

WORKDIR ${APP_ROOT}

RUN pip install pip --upgrade && pip install --no-cache-di -r requirements.txt

# # Collect static files
# RUN python manage.py collectstatic --noinput

# # Expose port 8000
# EXPOSE 8000

# # Run the entrypoint script to wait for the database to be ready before starting the server
# COPY ./docker-entrypoint.sh /docker-entrypoint.sh
# RUN chmod +x /docker-entrypoint.sh
# ENTRYPOINT ["/docker-entrypoint.sh"]

# # Run the Django app using gunicorn
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "qmeter.wsgi:application"]