FROM python:3.7

RUN mkdir /app/ && mkdir /app/templates/

WORKDIR /app/

#Add importants files
ADD templates/ ./templates/
ADD requirements.txt .
ADD CoinGecko.py .
ADD server.py .

# Install dependencies.
RUN pip install -r requirements.txt