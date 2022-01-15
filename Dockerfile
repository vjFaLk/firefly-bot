FROM python:3.8-slim-buster

WORKDIR /app
ENV CONFIG_PATH=/config

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src .

CMD [ "python", "/app/bot.py" ]
VOLUME [ "/config" ]
