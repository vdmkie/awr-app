FROM python:3.11-slim

# Установка системных зависимостей (для pandas, Pillow и др.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Установка pip и wheel последних версий (убирает много ошибок при сборке)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Копирование файла зависимостей
COPY requirements.txt .

# Установка Python-зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всех файлов приложения
COPY . .

# Создание необходимых директорий (если их нет)
RUN mkdir -p data uploads/uploads/photos static/css static/js static/images templates backups

# Указываем переменные окружения
ENV FLASK_ENV=production \
    PORT=5000 \
    PYTHONUNBUFFERED=1

# Открытие порта
EXPOSE 5000

# Запуск приложения
CMD ["python", "app.py"]
