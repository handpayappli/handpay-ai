# On part d'une version stable de Python
FROM python:3.10-slim

# On installe les bibliothèques graphiques manquantes (C'est ça qui bloquait !)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# On installe ton code
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# On lance le serveur
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:10000"]