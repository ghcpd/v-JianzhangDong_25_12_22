FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Create and activate venv, install dependencies
RUN python -m venv /opt/venv \
    && /opt/venv/bin/python -m pip install --upgrade pip setuptools wheel \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

# Default command: run tests
CMD ["/opt/venv/bin/python", "auto_test.py"]
