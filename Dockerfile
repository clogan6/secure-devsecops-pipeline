FROM python:3.14-slim

WORKDIR /app

# Install application dependencies
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Create a non-root user
RUN adduser --disabled-password --gecos "" appuser

# Copy application code
COPY --chown=appuser:appuser app/ ./app/

# Run as non-root
USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.app:app"]
