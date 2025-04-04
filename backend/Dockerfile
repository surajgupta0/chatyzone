# ------------------------------
# Stage 1: Install dependencies
# ------------------------------
FROM python:3.12 AS base

# Set the working directory
WORKDIR /var/www/html/portfolio/backend

# Set environment variables for better performance
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Install Poetry
RUN pip install poetry

# Copy dependency files first (to leverage Docker caching)
COPY poetry.lock pyproject.toml app.py ./

# Install dependencies **without virtualenv**
RUN poetry install --no-root --no-dev

# ------------------------------
# Stage 2: Build final production image
# ------------------------------
FROM python:3.12-slim AS production

# Set the working directory
WORKDIR /var/www/html/portfolio/backend

# Copy only necessary files from the base stage
COPY --from=base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=base /var/www/html/portfolio/backend /var/www/html/portfolio/backend

# Create a non-root user for security
RUN groupadd -g 1001 appgroup && useradd -u 1001 -g appgroup appuser
USER appuser

# Copy application source code
COPY src/ src/

# Expose the FastAPI port
EXPOSE 8000

CMD ["python", "app.py"]
