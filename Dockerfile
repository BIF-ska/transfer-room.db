# Use Python as base image
FROM python:3.9

# Set working directory inside the container
WORKDIR /app

# Install required system dependencies (ODBC & utilities)
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    curl \
    gnupg2 \
    unixodbc \
    unixodbc-dev

# Add Microsoft repository key
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg

# Add the Microsoft repository
RUN echo "deb [signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" | tee /etc/apt/sources.list.d/mssql-release.list

# Install ODBC Driver 17 for SQL Server
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Ensure ODBC Driver is correctly registered
RUN [ ! -f /usr/lib/libmsodbcsql-17.so ] && ln -s /opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.so /usr/lib/libmsodbcsql-17.so || echo "Symlink already exists"


# Verify ODBC installation
RUN odbcinst -q -d

# Copy only essential files first (to use Docker caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the project files
COPY . /app/

# Set default command to run the scheduler
CMD ["python", "/app/scheduler.py"]
