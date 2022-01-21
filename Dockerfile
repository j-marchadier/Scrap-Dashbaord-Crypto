FROM python:3.9

# Install dependencies.
ADD requirements.txt .
RUN pip update | pip upgrade | pip install -r requirements.txt

# Add actual source code.
ADD CoinGecko.py .

EXPOSE 8887

CMD ["python", "CoinGecko.py"]
