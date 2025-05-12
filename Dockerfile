FROM python:3.10-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    curl unzip wget gnupg ca-certificates \
    chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Удаляем старый Chromedriver
RUN rm -f /usr/bin/chromedriver

# Скачиваем ChromeDriver 136
RUN wget https://storage.googleapis.com/chrome-for-testing-public/136.0.7103.39/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm -rf chromedriver-linux64.zip chromedriver-linux64

ENV CHROME_BIN=/usr/bin/chromium
ENV PATH=$PATH:/usr/bin/chromedriver

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]
