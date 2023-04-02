#!/bin/bash

docker run --name development_db -e POSTGRES_PASSWORD=password -e POSTGRES_USER=user -e POSTGRES_DB=story_tracking -p 5432:5432 -d postgres