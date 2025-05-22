FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  default-libmysqlclient-dev \
  build-essential \
  pkg-config \
  python3-dev \
  default-mysql-client \
  netcat-traditional \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create media directory
RUN mkdir -p media

# Expose port
EXPOSE 8000

# # Run migrations
# RUN python manage.py migrate

RUN python3 -m pip install --upgrade pip
RUN apt-get update && apt-get install -y curl
RUN curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
  && chmod +x /usr/local/bin/docker-compose
RUN chmod +x ~/docker-compose

# Run the application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
