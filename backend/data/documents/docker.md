# Docker Fundamentals

Docker is a containerization platform that packages applications together with their dependencies into lightweight containers.

Containers provide consistency across development, testing, and production environments.

## Images

A Docker image is a read-only template used to create containers. Images are built from Dockerfiles.

Each instruction inside a Dockerfile creates a new image layer.

Smaller images generally build faster and consume less storage.

## Containers

A container is a running instance of an image.

Containers are isolated from one another but can communicate through Docker networks.

Containers can mount volumes to persist data outside the container lifecycle.

## Docker Compose

Docker Compose allows developers to define multi-container applications using a YAML configuration file.

A typical backend stack may include:

- FastAPI
- PostgreSQL
- Redis
- Qdrant
- Grafana
- Prometheus

Compose starts all services together and manages networking automatically.

## Best Practices

Use multi-stage builds to reduce image size.

Avoid storing secrets inside Docker images.

Keep containers stateless whenever possible.

Use health checks to monitor service availability.