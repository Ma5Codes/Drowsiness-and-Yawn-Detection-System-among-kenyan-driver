# Use an official Python image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential libssl-dev libffi-dev python3-venv libgl1-mesa-glx

# Copy project files
COPY . .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Expose the required port (Change this if needed)
EXPOSE 8000

# Start the application (Change this if needed)
CMD ["gunicorn", "drowsiness_project.wsgi:application", "--bind", "0.0.0.0:8000"]
