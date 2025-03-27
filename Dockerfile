# Use Python as base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Install dependencies and system utilities
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    curl \
    gnupg2 \
    unixodbc \
    unixodbc-dev \
    cron \
    nano \
    vim \
    dos2unix

# Install Microsoft ODBC driver
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" | tee /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Ensure ODBC driver symlink exists
RUN [ ! -f /usr/lib/libmsodbcsql-17.so ] && ln -s /opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.so /usr/lib/libmsodbcsql-17.so || echo "Symlink already exists"

# Show installed ODBC drivers (optional debug)
RUN odbcinst -q -d

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Only convert .env if it exists — avoids build crash
RUN [ -f /app/.env ] && dos2unix /app/.env || echo ".env not found, skipping dos2unix"

# Ensure cron log exists
RUN touch /var/log/cron.log

# Final CMD: Register midnight cron job, start cron, and stream logs
CMD bash -c "echo '0 0 * * * /usr/local/bin/python3 /app/python_code/util/scheduler.py >> /var/log/cron.log 2>&1' | crontab - && cron && tail -f /var/log/cron.log"
