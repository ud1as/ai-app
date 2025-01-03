FROM python:3.11

# Set the working directory
WORKDIR /app

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy the Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install the dependencies
RUN pipenv install --system --deploy

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python3", "main.py"]