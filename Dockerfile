FROM ubuntu:22.04

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy your repo into the container
COPY . /app

# Install dependencies if requirements.txt exists
RUN if [ -f requirements.txt ]; then pip3 install -r requirements.txt; fi

# Default command runs cron.py
CMD ["python3", "cron.py"]
