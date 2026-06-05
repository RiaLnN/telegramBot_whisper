FROM python:3-slim

WORKDIR /app
COPY bot/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ .

EXPOSE 80

CMD ["python", "main.py"]