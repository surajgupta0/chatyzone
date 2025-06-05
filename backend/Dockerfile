FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends libmagic1 && rm -rf /var/lib/apt/lists/*
RUN ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime

# Set the working directory
WORKDIR /var/www/html/chatifizer/backend

# Install Poetry
RUN pip install --no-cache-dir poetry beanie

# Copy dependency files first (to leverage Docker caching)
COPY poetry.lock pyproject.toml app.py ./

# Install dependencies **without virtualenv**
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main

COPY src/ ./src/

# Expose the FastAPI port
EXPOSE 8000

# CMD ["echo", "hello"]
CMD ["python", "app.py"]
