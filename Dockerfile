FROM python:3.9

RUN mkdir /app/ && mkdir /app/templates/

WORKDIR /app/
# Install dependencies.
ADD templates/ ./templates/
ADD requirements.txt .
ADD CoinGecko.py .
ADD server.py .

RUN pip update | pip upgrade | pip install -r requirements.txt