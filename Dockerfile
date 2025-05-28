FROM python:3.9

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    curl \
    gnupg2 \
    unixodbc \
    unixodbc-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    default-libmysqlclient-dev \
    nano vim dos2unix git

# Install Microsoft ODBC Driver 17 for SQL Server
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Set environment
ENV AIRFLOW_HOME=/app/airflow
ENV PYTHONPATH=/app

# Copy files early
COPY . /app/

COPY requirements.txt /app/
RUN pip install --no-cache-dir Flask-Session==0.5.0 && \
    pip install --no-cache-dir apache-airflow==2.8.1 && \
    pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/airflow/dags

# Entrypoint
ENTRYPOINT ["bash"]
CMD ["-c", "airflow db migrate && airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com --password airflow123 && airflow scheduler & airflow webserver -p 8080"]
