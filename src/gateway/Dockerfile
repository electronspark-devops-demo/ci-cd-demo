FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install Flask and requests
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy application code
COPY . /app

# Expose port 80 and run the Flask application
EXPOSE 80
CMD ["python", "app.py"]
