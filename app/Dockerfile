# Start from an official, lightweight Python base image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy just the requirements file first (see explanation below)
COPY code/requirements.txt .

# Install the Python packages needed to run the app
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application code
COPY code/ .

# Tell Docker which port the app will be listening on
EXPOSE 8050

# The command that actually starts the app when the container runs
CMD ["python", "app.py"]