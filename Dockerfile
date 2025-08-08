# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies required by WeasyPrint
RUN apt-get update && apt-get install -y \
    libpangocairo-1.0-0 \
    libgobject-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /code

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# --- ADD THIS LINE ---
# The command to run when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:10000"]
