# Use Python as base image
FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y \
    apt-transport-https \
    curl \
    gnupg2 \
    unixodbc \
    unixodbc-dev \
    cron  \
    nano  \
    vim  

RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg

RUN echo "deb [signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" | tee /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

RUN [ ! -f /usr/lib/libmsodbcsql-17.so ] && ln -s /opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.so /usr/lib/libmsodbcsql-17.so || echo "Symlink already exists"

RUN odbcinst -q -d

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/



RUN echo "0 0 * * * python /app/scheduler.py >> /var/log/cron.log 2>&1" > /etc/cron.d/scheduler_cronjob
RUN chmod 0644 /etc/cron.d/scheduler_cronjob
RUN crontab /etc/cron.d/scheduler_cronjob

# Create and start cron log
RUN touch /var/log/cron.log  
RUN service cron start  

CMD cron && tail -f /var/log/cron.log
