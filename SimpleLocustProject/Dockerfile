# Stage 1: Build dependencies
FROM python:3.9-slim as builder

WORKDIR /opt/locust

# Install necessary dependencies (only in build stage)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libev-dev \
    libffi-dev \
    libssl-dev \
    && pip install --upgrade pip \
    && pip install --no-cache-dir locust pyyaml \
    && apt-get remove -y build-essential gcc libev-dev libffi-dev libssl-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Final lightweight image
FROM python:3.9-slim

WORKDIR /opt/locust

# Copy only the required Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy only necessary Locust files
COPY simulations/ /opt/locust/simulations/
COPY constants/ /opt/locust/constants/
COPY util/ /opt/locust/util/
COPY environments/ /opt/locust/environments/
COPY runner/  /opt/locust/runner
COPY reports/ /opt/locust/reports

# Set environment variables for Locust
ENV LOCUST_HEADLESS=true
ENV LOCUST_USERS=1
ENV LOCUST_SPAWN_RATE=1
ENV LOCUST_RUN_TIME=1m

# Default command
ENTRYPOINT ["python"]