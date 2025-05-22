FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
  default-libmysqlclient-dev \
  build-essential \
  pkg-config \
  python3-dev \
  default-mysql-client \
  netcat-traditional \
  && rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Создание директории для медиафайлов
RUN mkdir -p media

# Открытие порта
EXPOSE 8000

# Запуск приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]