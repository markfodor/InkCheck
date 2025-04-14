FROM mcr.microsoft.com/playwright/python:v1.51.0-noble

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc g++ python3-dev \
    && apt-get clean

WORKDIR /inkcheck
COPY requirements.txt .

# Install dependencies
RUN python3 -m pip install --upgrade pip \
    && pip3 install --no-cache-dir --upgrade -r requirements.txt

RUN playwright install

COPY . .
EXPOSE 8080
ENTRYPOINT ["python3", "main.py"]
