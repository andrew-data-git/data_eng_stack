FROM ubuntu:latest

# Install dependencies
RUN echo 'Installing dependencies.'
RUN apt-get update && apt-get install -y \
    cron \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files
RUN echo 'Copying files.'
COPY main.py .
COPY requirements.txt .
COPY crontab.txt .
COPY run.sh .
COPY .env .

# Install Python dependencies
RUN echo 'Python dependencies.'
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
ENV PATH="/opt/venv/bin:$PATH"

# Set up cron job
RUN echo 'Setting up cron job'
RUN chmod +x run.sh
RUN crontab crontab.txt
RUN touch /var/log/cron.log

# Run both cron and tail log to keep container alive
RUN echo 'GO!'
CMD cron && tail -f /var/log/cron.log
