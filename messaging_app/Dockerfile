# Dockerfile

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

# Install MySQL client dependencies + Python deps
RUN apt-get update && apt-get install -y bash\
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-openbsd \
    default-mysql-client \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh


EXPOSE 8000

CMD ["/wait-for-db.sh", "db", "python", "manage.py", "runserver", "0.0.0.0:8000"]

# docker run -p 8000:8000 messaging_app_image
