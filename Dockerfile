# Use an official Python runtime as a base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the required Python packages
RUN pip install -r requirements.txt

# Run the application
CMD ["python", "server.py"]

# Expose the port that the app runs on
EXPOSE 80
