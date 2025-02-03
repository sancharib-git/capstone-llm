FROM mcr.microsoft.com/vscode/devcontainers/python:3.13-bookworm 

USER root

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install Java 11
RUN apt-get update && apt-get install -y openjdk-17-jdk

# Install Conveyor
RUN curl -s https://static.conveyordata.com/cli-install/install.sh | bash

# Install AWS CLI
RUN wget "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -O "awscliv2.zip" && \
    unzip awscliv2.zip && \
    rm -rf awscliv2.zip && \
    sudo ./aws/install --install-dir /opt/aws-cli --bin-dir /usr/local/bin/ && \
    sudo chmod a+x /opt/

USER vscode