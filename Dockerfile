# Minimal reproducible container for running project tests
FROM python:3.14-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt
COPY . .
# default: run the shell test script
CMD ["/bin/bash", "-lc", "./run_test.sh"]
