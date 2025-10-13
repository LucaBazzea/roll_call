FROM python:3.12-alpine

# Set the working directory
WORKDIR /app

# Copy only the requirements first (for layer caching)
COPY requirements.txt .

# Install system dependencies and Python packages
RUN apk add --no-cache build-base \
  && pip install --no-cache-dir -r requirements.txt \
  && apk del build-base

# Copy the application code
COPY . .

# Copy .env if you need it inside the container
COPY .env /app/.env
RUN chmod +r /app/.env || true

# Expose Django port
EXPOSE 8000

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
