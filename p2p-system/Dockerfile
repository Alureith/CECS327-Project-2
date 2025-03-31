# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy your app code into the container
COPY . .

# Install Flask directly
RUN pip install flask

# Expose the Flask port
EXPOSE 5000

# Run the app
CMD ["python", "node.py"]
