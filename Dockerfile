# 1) Базовый образ с Python и Debian
FROM python:3.10-slim

# 2) Устанавливаем Chrome и зависимости для Selenium
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
       wget \
       unzip \
       chromium-driver \
       chromium \
       ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# 3) Копируем код приложения
WORKDIR /app
COPY . /app

# 4) Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 5) Экспонируем порт, который слушает Flask
EXPOSE 5000

# 6) По умолчанию запускаем gunicorn
CMD ["gunicorn", "server:app", "--bind", "0.0.0.0:5000", "--workers", "1"]
