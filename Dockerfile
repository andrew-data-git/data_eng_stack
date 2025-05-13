FROM python:3.11-slim

# Set working directory, copy scripts
WORKDIR /app
COPY main.py .
COPY requirements.txt .
COPY crontab.txt .

# Py packages
RUN pip install --no-cache-dir -r requirements.txt

# Set up cron job
RUN apt-get update && apt-get install -y cron
RUN crontab crontab.txt

# Ensure log file exists
RUN touch /var/log/cron.log

# Start cron in foreground
CMD ["cron", "-f"]
