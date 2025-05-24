FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install system dependencies (build essentials and curl)
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH (assuming default install location)
ENV PATH="/root/.local/bin:$PATH"

# Copy only poetry files first for better caching
COPY poetry.lock pyproject.toml /app/

# Copy the rest of the project files
COPY . .

# Install only dependencies (skip installing project as package)
RUN poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

# Collect static files
# RUN python manage.py collectstatic --noinput

# Expose port 8000 (Django default)
EXPOSE 8000

# Run the app with gunicorn
CMD ["gunicorn", "portfolio.wsgi:application", "--bind", "0.0.0.0:8000"]
