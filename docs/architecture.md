# askcos2_core Architecture

```mermaid
C4Context

title ASKCOSv2 Architecture

Person_Ext(user, "User", "Uses the ASKCOSv2 API to generate reactions")

System_Boundary(host, "Host Machine") {
    System(nginx, "Nginx", "Serves the ASKCOSv2 API and Vue frontend")

    Container_Boundary(docker, "Docker Containers") {
        Container(api, "API", "Runs the ASKCOSv2 API")
        Container(precompute, "Precompute", "Runs precompute tasks")
        Container(celery, "Celery", "Runs Celery workers")
        ContainerDb(mongo, "MongoDB", "Stores the ASKCOSv2 database")
        Container(redis, "Redis", "Caches data")
        ContainerQueue(rabbitmq, "RabbitMQ", "Handles Celery tasks")
    }
}

Rel_Down(user, nginx, "HTTP/S")
Rel_Down(nginx, api, "HTTP/S")
Rel_Up(rabbitmq, celery, "Queue Tasks")
Rel_Down(api, mongo, "Data")
Rel_Down(api, rabbitmq, "Queue Tasks")
UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```
