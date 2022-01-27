FROM python:3.7

RUN mkdir /app/ && mkdir /app/templates/

WORKDIR /app/
# Install dependencies.
ADD templates/ ./templates/
ADD requirements.txt .
ADD CoinGecko.py .
ADD server.py .
ADD AirPassengers.csv .

RUN pip update | pip upgrade | pip install -r requirements.txt