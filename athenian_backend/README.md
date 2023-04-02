# Backend service

## API Documentation:
(http://localhost:8000/api/schema/swagger-ui/)[http://localhost:8000/api/schema/swagger-ui/]

## Running just the backend with docker

First one must build the image

```
.\scripts\build_image.sh
```

After that, you can use the docker-compose

```
docker-compose up
```

## Running tests

```
python manage.py test
```