# Use Python as base image
FROM python:3.9

# Set working directory inside the container
WORKDIR /app

# Copy only essential files first
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the project files
COPY . /app/

# Set default command to run the scheduler
CMD ["python", "/app/scheduler.py"]
