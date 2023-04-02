# Frontend service

## Running the frontend with docker

First build the image

```
.\scripts\build_image.sh
```

After that, you can just lauch the container

```
docker container run -p 3000:3000 athenian_frontend:latest
```

The frontend will be running at localhost:3000