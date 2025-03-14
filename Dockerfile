# Use Python as base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit UI (if using Streamlit)
EXPOSE 8501

# Start the scheduler script automatically
CMD ["python", "scheduler.py"]
