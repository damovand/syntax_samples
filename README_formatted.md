## The following are samples of various syntax
### These are all captured through online searches.


### Basic Healthcheck Structure
Docker Compose supports healthchecks directly inside a service definition. The main fields are:

  | test — command to run (CMD or CMD-SHELL).
  | interval — how often the check runs.
  | timeout — max time allowed for the check.
  | retries — number of failures before marking unhealthy.
  | start_period — grace period before checks count as failures.

### Example: Web App Healthcheck
##### If your service exposes an HTTP /health or /status endpoint, you can start with this simple health check. It works well for most HTTP-based applications
services:
  app:
    image: myapp:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
     
    #### This checks an HTTP endpoint and marks the container healthy only when it returns success.


### This checks an HTTP endpoint and marks the container healthy only when it returns success.

services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: changeme
      POSTGRES_DB: myapp
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

    ## This uses pg_isready to verify the database is accepting connections.

### Example: Redis Healthcheck
services:
  redis:
    image: redis
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 1s
      timeout: 3s
      retries: 30


### Using depends_on with service_healthy

services:
  app:
    build: .
    depends_on:
      db:
        condition: service_healthy
