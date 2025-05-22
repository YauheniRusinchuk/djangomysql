# Этап сборки зависимостей
FROM python:3.11-slim as builder

WORKDIR /app

# Установка системных зависимостей для сборки
RUN apt-get update && apt-get install -y \
  gcc \
  python3-dev \
  default-libmysqlclient-dev \
  pkg-config \
  && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей с кэшированием
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Финальный образ
FROM python:3.11-slim

WORKDIR /app

# Установка runtime зависимостей
RUN apt-get update && apt-get install -y \
  libmariadb3 \
  netcat-traditional \
  && rm -rf /var/lib/apt/lists/*

# Создание непривилегированного пользователя
RUN useradd --create-home appuser && \
  chown -R appuser:appuser /app
USER appuser

# Настройка окружения
ENV PATH="/home/appuser/.local/bin:${PATH}" \
  PYTHONPATH="${PYTHONPATH}:/app" \
  PYTHONUNBUFFERED=1

# Копирование зависимостей из builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Копирование проекта
COPY --chown=appuser:appuser . .

# Сборка статики и подготовка
RUN mkdir -p media staticfiles && \
  python manage.py collectstatic --noinput --clear && \
  find . -type d -name "__pycache__" -exec rm -rf {} +

# Порт
EXPOSE 8000

# Команда запуска с настройкой для Railway
CMD ["gunicorn", \
  "--bind", "0.0.0.0:8000", \
  "--workers", "3", \
  "--timeout", "120", \
  "--preload", \
  "core.wsgi"]