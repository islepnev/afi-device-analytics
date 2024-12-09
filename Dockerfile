# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files
COPY requirements.txt ./
COPY .env.example .env
COPY app/ ./app/
COPY manage.py ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the app runs on
EXPOSE 5000

# Set the entry point for the container
CMD ["python", "manage.py"]
