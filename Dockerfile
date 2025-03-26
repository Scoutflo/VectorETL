# Use an official Python image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --upgrade vector-etl

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the FastAPI server port
EXPOSE 8000

# Command to run the server
CMD ["python", "etl_server.py"]
