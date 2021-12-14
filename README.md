# ICG Controller

This repository contains all the required code and templates to run the ICG component, it also contains a Dockerfile that builds the complete image of the ICG with a provided REST API

Installation
-------------

To have a functional ICG application the following steps can be used.
    - Download the full content of this repository
    - Build the doxker image launching inside the downloaded folder the command: docker build .
    - Create a volume for the container: docker volume create ICG-volume
    - Run the container: docker run --mount source=ICG-volume,target=/opt -p 5000:5000 <image_name>

User manual
------------

To use the now running ICG docker container we can call the available REST API.

The API is available in loccalhost at port 5000, the application path "/". (ex: http://localhost:5000/)
Sending a post request at this endpoint with the indicated json body (see parameters.json as an example body) it will respond with a .tar.gz file containing all the required IaC files.