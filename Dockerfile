FROM python:3.10-slim

# Устанавливаем Chromium и Chromedriver (совпадающие версии)
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    python3-pip \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Пропишем команду запуска
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]
