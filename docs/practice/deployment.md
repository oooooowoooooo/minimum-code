# Deployment

## From Development to Production

The gap between "it works on my machine" and "it works in production" is where most projects stumble. This chapter bridges that gap.

Deployment is not just about getting code onto a server. It is about creating a system that is reliable, observable, and maintainable in the real world.

## Docker Containerization

### Why Docker

Docker solves the "works on my machine" problem by packaging your application with its dependencies. Every environment runs the same code, the same libraries, the same configuration format.

### Backend Dockerfile

```
Generate a production-ready Dockerfile for the Python FastAPI backend.

Requirements:
- Multi-stage build (builder stage + production stage)
- Python 3.11-slim as base
- Install only production dependencies (no dev tools in final image)
- Non-root user for security
- Copy only necessary files
- Health check endpoint
- Proper signal handling (uvicorn with --proxy-headers)
- Expose port 8000
- Environment variable for configuration

The Dockerfile should:
1. Use a builder stage to install dependencies
2. Copy only the installed packages and application code to the production stage
3. Run as a non-root user named "app"
4. Include a HEALTHCHECK instruction
5. Use ENTRYPOINT for the main process and CMD for default arguments
```

### Frontend Dockerfile

```
Generate a production-ready Dockerfile for the Next.js frontend.

Requirements:
- Multi-stage build (deps -> build -> production)
- Node 20-alpine as base
- Install dependencies separately from application code (for caching)
- Build the Next.js application
- Use standalone output mode for minimal production image
- Non-root user
- Expose port 3000
- Health check
```

### Docker Compose

```
Generate a docker-compose.yml for local development and testing.

Services:
1. postgres:
   - Image: postgres:16 with pgvector extension
   - Volume for data persistence
   - Health check
   - Environment: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB

2. backend:
   - Build from backend/Dockerfile
   - Depends on postgres (wait for healthy)
   - Environment: DATABASE_URL, JWT_SECRET, API keys
   - Volume mount for uploads
   - Port mapping: 8000:8000

3. frontend:
   - Build from frontend/Dockerfile
   - Depends on backend
   - Environment: NEXT_PUBLIC_API_URL
   - Port mapping: 3000:3000

Include:
- A shared network for all services
- Named volumes for postgres data and uploads
- Restart policies (unless-stopped)
- Proper health checks for dependency ordering
```

## CI/CD Pipeline

### GitHub Actions Workflow

```
Generate a GitHub Actions CI/CD workflow.

Triggers:
- Push to main branch
- Pull requests to main branch

Jobs:

1. lint-and-type-check:
   - Run ruff for Python linting
   - Run mypy or pyright for Python type checking
   - Run ESLint for TypeScript/React
   - Run TypeScript compiler for type checking
   - All must pass before proceeding

2. test-backend:
   - Set up Python 3.11
   - Start PostgreSQL service container
   - Install dependencies
   - Run pytest with coverage
   - Upload coverage report

3. test-frontend:
   - Set up Node.js 20
   - Install dependencies
   - Run Vitest with coverage
   - Upload coverage report

4. build:
   - Depends on lint, test-backend, test-frontend
   - Build backend Docker image
   - Build frontend Docker image
   - Push images to container registry (on main branch only)

5. deploy (main branch only):
   - Depends on build
   - Deploy to hosting platform
   - Run smoke tests
   - Notify on success/failure

Use GitHub secrets for:
- Database credentials
- API keys
- Container registry credentials
- Deployment credentials
```

### Environment Configuration

```
Generate environment configuration files:

1. .env.example - Template with all required variables (no real values):
   # Database
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/knowledge_base

   # Authentication
   JWT_SECRET=change-me-to-a-random-string
   JWT_ALGORITHM=HS256
   JWT_EXPIRY_MINUTES=15

   # AI Services
   EMBEDDING_API_KEY=your-api-key
   EMBEDDING_MODEL=text-embedding-3-small
   LLM_API_KEY=your-api-key
   LLM_MODEL=gpt-4o-mini

   # Application
   UPLOAD_DIR=./uploads
   MAX_FILE_SIZE_MB=50
   CORS_ORIGINS=http://localhost:3000

2. .env.production - Production values (placeholder, never committed)

3. .env.test - Test configuration (uses test database, mock API keys)

Also generate .gitignore entries for all .env files except .env.example.
```

## Monitoring and Observability

### Structured Logging

```
Implement structured logging for the backend:

Requirements:
- JSON format for all log output
- Include in every log entry:
  - timestamp (ISO 8601)
  - level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - message
  - request_id (UUID, generated per request)
  - user_id (if authenticated)
  - duration_ms (for operation timing)
  - Additional context fields as needed

Implementation:
- Use Python's structlog library
- Create middleware that adds request_id to each request context
- Log request start and end with method, path, status code, and duration
- Log errors with full stack trace and context
- Never log sensitive data (passwords, tokens, API keys)

Log levels:
- DEBUG: Detailed information for debugging
- INFO: Normal operations (request processed, document uploaded)
- WARNING: Unexpected but handled (retry succeeded, fallback used)
- ERROR: Operation failed (document processing failed, API error)
- CRITICAL: System-level failure (database connection lost, out of memory)
```

### Health Check Endpoint

```
Implement a health check endpoint:

GET /health

Response (healthy):
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00Z",
    "checks": {
        "database": { "status": "up", "latency_ms": 5 },
        "embedding_api": { "status": "up", "latency_ms": 120 },
        "llm_api": { "status": "up", "latency_ms": 200 }
    }
}

Response (unhealthy):
{
    "status": "unhealthy",
    "timestamp": "2024-01-15T10:30:00Z",
    "checks": {
        "database": { "status": "up", "latency_ms": 5 },
        "embedding_api": { "status": "down", "error": "Connection refused" },
        "llm_api": { "status": "up", "latency_ms": 200 }
    }
}

This endpoint is used by Docker health checks and monitoring systems.
It should not require authentication.
```

### Key Metrics to Track

```
Implement basic metrics collection:

1. Request metrics:
   - Request count by method and path
   - Response time percentiles (p50, p95, p99)
   - Error rate (4xx and 5xx responses)
   - Active request count

2. Business metrics:
   - Document upload count (by type)
   - Query count
   - Average query response time
   - Embedding generation time

3. System metrics:
   - Database connection pool usage
   - Memory usage
   - CPU usage
   - Disk usage (uploads directory)

Expose metrics at GET /metrics in Prometheus format.
Use prometheus_client library for Python.
```

## Production Readiness Checklist

Before going live, verify every item:

### Security

```
[ ] All secrets are in environment variables, not in code
[ ] HTTPS is enforced (redirect HTTP to HTTPS)
[ ] CORS is configured for specific origins, not *
[ ] Rate limiting is enabled on all endpoints
[ ] Input validation is comprehensive
[ ] SQL injection protection (ORM usage verified)
[ ] XSS protection (output encoding verified)
[ ] JWT tokens have appropriate expiry
[ ] Password hashing uses bcrypt with adequate cost factor
[ ] File upload validation is strict (type, size, content)
[ ] Error responses do not leak internal details
[ ] Dependency vulnerabilities scanned (pip-audit, npm audit)
```

### Reliability

```
[ ] Database migrations are tested and reversible
[ ] Connection pooling is configured
[ ] Retry logic for external API calls
[ ] Graceful shutdown handles in-flight requests
[ ] Health check endpoint is working
[ ] Error handling covers all failure modes
[ ] Resource limits are set (file size, query rate, etc.)
[ ] Backup strategy for database is in place
[ ] Recovery procedure is documented and tested
```

### Performance

```
[ ] Database queries are optimized (indexes verified)
[ ] N+1 query problems are eliminated
[ ] Caching is implemented where appropriate
[ ] File uploads are streamed, not loaded into memory
[ ] Embedding generation is batched
[ ] Static assets are served via CDN or reverse proxy
[ ] Connection timeouts are configured
```

### Observability

```
[ ] Structured logging is in place
[ ] Error tracking is configured (Sentry or similar)
[ ] Key metrics are collected and displayed
[ ] Alerts are configured for critical issues
[ ] Request tracing is implemented (request IDs)
[ ] Log retention policy is defined
```

### Operations

```
[ ] Deployment process is documented
[ ] Rollback procedure is documented
[ ] Database migration process is documented
[ ] Scaling procedure is documented
[ ] Incident response plan exists
[ ] On-call rotation is defined (if applicable)
```

## Deployment Strategies

### Simple Deployment (Single Server)

For a first deployment, keep it simple:

```
1. Rent a VPS (e.g., DigitalOcean, Hetzner, AWS Lightsail)
2. Install Docker and Docker Compose
3. Clone the repository
4. Configure environment variables
5. Run docker-compose up -d
6. Set up nginx as reverse proxy (SSL termination, static files)
7. Set up certbot for HTTPS certificates
8. Configure systemd for auto-restart on reboot
```

### Using AI for Deployment

```
I need to deploy my application to [platform]. Here is my docker-compose.yml:

[paste docker-compose.yml]

Generate:
1. Step-by-step deployment instructions
2. Nginx configuration for reverse proxy
3. Systemd service file for auto-restart
4. SSL certificate setup with certbot
5. Basic monitoring setup
```

### Cloud Deployment

When you outgrow a single server:

```
Database: Managed PostgreSQL (AWS RDS, Google Cloud SQL, Supabase)
Backend: Container service (AWS ECS, Google Cloud Run, Railway)
Frontend: Static hosting (Vercel, Netlify, Cloudflare Pages)
File storage: Object storage (AWS S3, Google Cloud Storage)
Secrets: Secret manager (AWS Secrets Manager, Doppler)
```

## Post-Deployment

### Monitoring Dashboard

Set up a basic monitoring dashboard:

```
Key views:
1. Overview: Request count, error rate, response time (last 24h)
2. Errors: Error log, error rate by endpoint, recent stack traces
3. Performance: Response time percentiles, slow queries, API latency
4. Business: Documents uploaded, queries made, active users
5. System: CPU, memory, disk, database connections
```

### Incident Response

When something breaks in production:

```
1. Detect: Monitoring alerts you (or users report issues)
2. Assess: Check health endpoint, review recent logs, identify scope
3. Mitigate: Restart service, rollback deployment, scale up
4. Resolve: Fix the root cause, test the fix
5. Review: Write a post-mortem, identify preventive measures

Key questions during an incident:
- When did it start? (Check deployment timestamps)
- What changed? (Recent deployments, config changes, external service changes)
- Who is affected? (All users, specific users, specific features)
- What is the impact? (Complete outage, degraded performance, data loss)
```

## Summary

Deployment is the final stage of the development workflow, but it is not the end. Production software requires ongoing attention: monitoring, updates, scaling, and improvement.

The key principles:

1. **Automate everything.** Manual deployments are error-prone. CI/CD eliminates human error.
2. **Monitor proactively.** Do not wait for users to report problems. Set up alerts.
3. **Start simple.** A single server with Docker Compose is fine for the first version.
4. **Plan for failure.** Everything will fail eventually. Design for graceful degradation.
5. **Document operations.** If only one person knows how to deploy, you have a bus factor of one.

With this chapter, you have completed the full development lifecycle: planning, architecture, implementation, and deployment. The skills you have practiced transfer to any project, any technology, any team.
