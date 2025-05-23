#!/bin/bash
echo 'Cron called'
source /app/.env
/app/venv/bin/python3 /app/main.py >> /var/log/cron.log 2>&1
