FROM python:3.9.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8509

CMD ["python", "run.py"]

