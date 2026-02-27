FROM python:3.10-slim


RUN apt-get update && apt-get install -y \
    curl \
    tar \
    cpulimit \
    tor \
    torsocks \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY . .


RUN chmod 777 /app
CMD ["python3", "app.py"]
