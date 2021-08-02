FROM python:3.9-alpine

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Include the app code
COPY ./app /app
WORKDIR /app

# Run the app
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
