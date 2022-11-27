FROM registry.fedoraproject.org/fedora:latest AS base

LABEL maintainer="James Jones <jamjon3@gmail.com>"
LABEL description="This project illustrates a python app that uses an API \
to derive a download URL and download the target file."

# Install some dependencies
RUN dnf install -y rubygems ruby-devel gcc gcc-c++ make \
            libffi-devel python3 python3-pip python3-virtualenv python-unversioned-command

FROM base AS build

WORKDIR /output

# Copy over python related files
COPY *.py .
COPY requirements.txt .

# Setup a virtual environment for python
RUN python -m venv venv

# Gather pip dependencies
RUN source venv/bin/activate \
    && pip install -r requirements.txt

# Run the pyinstaller to build the app and all it's dependencies
RUN source venv/bin/activate \
    && exec python build.py

FROM base AS final

# Move the binary into /usr/bin
COPY --from=build --chown=root:root /output/dist/getlatestdownloadbinary /usr/bin/getlatestdownloadbinary

# Setup the entrypoint script
COPY entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]


