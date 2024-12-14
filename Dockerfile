# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for the app to be accessible
EXPOSE 8080

# # Set environment variables
# ENV FLASK_APP=app.py
# ENV FLASK_ENV=development

# Run the Flask app
# CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
CMD ["python", "app.py"]