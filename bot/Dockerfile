FROM python:3.11-slim

WORKDIR /app

COPY bot/requirements.txt ./bot/
RUN pip install --no-cache-dir -r ./bot/requirements.txt

COPY . .

RUN chmod +x bot/entrypoint.sh

ENV PYTHONPATH="/app"

CMD ["./bot/entrypoint.sh"]