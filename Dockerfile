FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD python3 -m uvicorn app.main:app --host 0.0.0.0 --log-level warning
EXPOSE 8000