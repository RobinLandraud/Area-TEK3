# Dockerization of the project #

This document describes how the project is deployed.
The project is deployed using [Docker](https://docs.docker.com/] and [Docker Compose](https://docs.docker.com/compose/).

## Docker Compose ##

The `docker-compose.yml` file is the main file that describes the project's services.

In this file, we define the services that compose the project, the networks they use, the volumes they use, and the environment variables they use.

### Services ###

Each service is defined by a block like this:
````yaml
    service_name:
      build:
        context: ./path/to/Dockerfile
        dockerfile: name of the Dockerfile
      command: ./command/to/run
      depends_on:
        - another_service_name
      ports:
        - 0000:0000
      networks:
        - network_name
      volumes:
        - ./path/to/volume:/path/to/volume
      environment:
        - VARIABLE_NAME=variable_value
````

### Volumes ###

You can add volumes like this:
````yaml
    volumes:
      - ./path/to/volume:/path/to/volume
````

### Networks ###

You can add Docker Networks like this:
````yaml
    networks:
      - network_name
````

## Dockerfile ##

The `Dockerfile` is the file that describes how the container is built.

In this file, we define the base image, the commands to run, the ports to expose, the volumes to use, and the environment variables to use.

## Create a new service ##

Create a folder service_name/ and add Dockerfile in it

### Example ###

You can add a Dockerfile like this:
````dockerfile
    FROM base_image

    ENV SERVICE_NAME_HOME /home/app/service_name
    RUN mkdir -p $SERVICE_NAME_HOME
    WORKDIR $SERVICE_NAME_HOME

    ENV PORT 0000

    COPY . $SERVICE_NAME_HOME

    EXPOSE $PORT
    VOLUME /path/to/volume
    RUN RUN ./command/to/run

````

