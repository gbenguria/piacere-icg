# ICG Controller

This repository contains all the required code and templates to run the ICG component, it also contains a Dockerfile that builds the complete image of the ICG with a provided REST API

Requirements
-------------
- Docker

Installation
-------------

To have a functional ICG application the following steps can be used.

- Download the full content of this repository
- Build the docker image launching the following command: `docker build -t icg:0.1 .` 
- Run the container: `docker run --name icg -d -p 5000:5000 icg:0.1`

Usage
------------

To use the now running ICG docker container we can call the available REST API.

The API is available at http://localhost:5000/docs. You can try here the endpoint behavior (see input_file_example/nginx/parameters.json as an example body).

Otherwise, send a POST request at this endpoint with the indicated json body (see input_file_example/nginx/parameters.json as an example body) it will respond with a .tar.gz file containing all the required IaC files:

    - curl --location --request POST localhost:5000/infrastructure/files --header "Content-Type: application/json" --data "@parameters.json" --output "OutputIaC.tar.gz"

Uninstall
------------
Remove the docker container and the docker image:

```
docker container rm -f icg
docker rmi icg:0.1
```