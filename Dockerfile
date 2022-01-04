FROM python:3.9

WORKDIR /scraping

# Install dependencies.
ADD requirements.txt /scraping
RUN cd /scraping && \
    pip install -r requirements.txt

# Add actual source code.
ADD main.py /scraping

EXPOSE 8887

CMD ["python", "main.py"]
