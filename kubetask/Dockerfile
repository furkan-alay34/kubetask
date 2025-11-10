# 1️⃣ Python 3.11 slim imajını kullan
FROM python:3.11-slim

# 2️⃣ Çalışma dizinini ayarla
WORKDIR /app

# 3️⃣ Gereken sistem paketlerini yükle (SQLite ve bağımlılıklar)
RUN apt-get update && \
    apt-get install -y sqlite3 && \
    rm -rf /var/lib/apt/lists/*

# 4️⃣ Uygulama dosyalarını kopyala
COPY . /app

# 5️⃣ Veritabanı için klasör oluştur
RUN mkdir -p /data

# 6️⃣ Eğer local’de demo.db varsa, onu /data içine taşı
# (örneğin proje dizininde demo.db varsa)
RUN if [ -f "demo.db" ]; then mv demo.db /data/demo.db; fi

# 7️⃣ Python bağımlılıklarını yükle
RUN pip install --no-cache-dir -r requirements.txt

# 8️⃣ Flask env ayarlarını yap
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# 9️⃣ Container açıldığında çalışacak komut
CMD ["flask", "run"]