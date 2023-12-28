FROM mcr.microsoft.com/devcontainers/python:0-3.10

USER root
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y vim tree \
    && apt-get install -y pre-commit \
    && apt-get clean  # This line cleans up the package lists to reduce image size

ENV USER=vscode
USER $USER

WORKDIR /home/$USER
COPY ./.docker_requirements.txt .
COPY ./.docker_requirements_scientific.txt .

ARG DOCKER_IMAGE_TYPE
RUN if [ "$DOCKER_IMAGE_TYPE" = "minimal" ]; then \
        pip install -r .docker_requirements.txt; \
    else \
        pip install -r .docker_requirements_scientific.txt; \
    fi
