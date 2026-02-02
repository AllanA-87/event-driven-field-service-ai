FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Using python main.py directly is often easier for debugging
CMD ["python", "main.py"]
