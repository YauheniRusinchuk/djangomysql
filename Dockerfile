# Этап сборки зависимостей
FROM python:3.11-slim as builder

WORKDIR /app

# Установка системных зависимостей для сборки
RUN apt-get update && apt-get install -y \
  gcc \
  python3-dev \
  default-libmysqlclient-dev \
  pkg-config \
  libssl-dev \
  && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Финальный образ
FROM python:3.11-slim

WORKDIR /app

# Установка runtime зависимостей и настройка прав
RUN apt-get update && apt-get install -y \
  libmariadb3 \
  netcat-traditional \
  && mkdir -p /app/staticfiles /app/media \
  && chmod -R 755 /app/staticfiles \
  && rm -rf /var/lib/apt/lists/*

# Создание пользователя и владение файлами
RUN useradd --create-home appuser \
  && chown -R appuser:appuser /app \
  && chmod -R 755 /app/staticfiles

USER appuser

# Копирование зависимостей из builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Копирование проекта
COPY --chown=appuser:appuser . .

# Настройка окружения
ENV PATH="/home/appuser/.local/bin:${PATH}" \
  PYTHONUNBUFFERED=1 \
  PYTHONPATH="/app"

# Сборка статики с подробным выводом
RUN python manage.py collectstatic --noinput --clear -v 3

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "core.wsgi"]