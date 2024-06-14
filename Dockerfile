FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
EXPOSE 8000