FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

# Start both Streamlit and the scheduler
CMD ["sh", "-c", "streamlit run app.py & python scheduler.py"]
