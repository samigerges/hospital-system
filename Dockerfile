FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN python - <<'PY'
from pathlib import Path
src = Path('/tmp/requirements.txt')
text = src.read_text(encoding='utf-16')
Path('/tmp/requirements-utf8.txt').write_text(text, encoding='utf-8')
PY
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements-utf8.txt

COPY . /app

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
