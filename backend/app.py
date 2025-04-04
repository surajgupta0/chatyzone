import os

# Environment check (default: development)
ENVIRONMENT = os.getenv("ENV", "development")  # 'development' or 'production'

if __name__ == "__main__":

    if ENVIRONMENT == "production":
        # Run Gunicorn in production (4 workers for handling concurrent requests)
        os.system(
            "gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app --bind 0.0.0.0:8000"
        )
    else:
        # Run Uvicorn in development (with auto-reload)
        os.system(
            "uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload"
        )