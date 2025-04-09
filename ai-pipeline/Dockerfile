FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure the model is included
COPY selector_model.pkl .

CMD ["python", "pipeline.py"]