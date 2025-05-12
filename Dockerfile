FROM python:3.11-slim

# Set the working directory inside the container, and copy the Python script into the container
WORKDIR /app
COPY main.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Run the script when the container starts
CMD ["python", "main.py"]
