FROM gitpod/workspace-python:latest

# Use the same python version as exists in Spark
RUN pyenv install 3.10.12 \
    && pyenv global 3.10.12

RUN wget "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -O "awscliv2.zip" && \
    unzip awscliv2.zip && \
    rm -rf awscliv2.zip && \
    sudo ./aws/install --install-dir /opt/aws-cli --bin-dir /usr/local/bin/ && \
    sudo chmod a+x /opt/

RUN curl -sSL https://install.python-poetry.org | python3 - && poetry config virtualenvs.in-project true