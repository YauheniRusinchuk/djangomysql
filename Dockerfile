# Этап сборки зависимостей
FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
  gcc \
  python3-dev \
  default-libmysqlclient-dev \
  pkg-config \
  libssl-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Финальный образ
FROM python:3.11-slim

WORKDIR /app

# Runtime зависимости и настройка прав
RUN apt-get update && apt-get install -y \
  libmariadb3 \
  netcat-traditional \
  && mkdir -p /app/staticfiles /app/media \
  && chmod -R 755 /app/staticfiles \
  && rm -rf /var/lib/apt/lists/*

# Создание пользователя и владение файлами
RUN useradd --create-home appuser \
  && chown -R appuser:appuser /app

USER appuser

# Копирование зависимостей
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Копирование проекта
COPY --chown=appuser:appuser . .

# Настройка окружения
ENV PATH="/home/appuser/.local/bin:${PATH}" \
  PYTHONUNBUFFERED=1 \
  PYTHONPATH="/app"

# Сборка статики с проверкой
RUN python manage.py collectstatic --noinput --clear || \
  (echo "Warning: Collectstatic failed! Check staticfiles configuration."; exit 0)

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "core.wsgi"]