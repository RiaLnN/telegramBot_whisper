FROM python:3-slim

WORKDIR /
COPY bot/requirements.txt ./bot/
RUN pip install --no-cache-dir -r ./bot/requirements.txt

COPY bot/ ./bot/
ENV PYTHONPATH="/"
EXPOSE 80

CMD ["python", "-m", "bot.main"]