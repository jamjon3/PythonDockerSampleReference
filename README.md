# PythonDockerSampleReference

## Description:

This sample app combines both options below

Option 1:
- Python coding exercise
- Write a small class that retrieves data from an API

Option 2:
- Practical docker exercise
- Candidate should have docker installed
- Will be working to set up and run a basic app (that will be created) in docker

## Option 1

The python app pulls the latest release from the GitHub API with a small class
as well as another small class for downloading te release binary.

## Option 2

Uses a docker container to 'build' the 'Option 1' basic app into a binary inside a container
using:

```docker build --target final --tag sample .```

This builds a container with the PyInstaller binary setup with an entrypoint
so it can be executed without specifying the binary:

```docker run -it --privileged -v $(pwd):/tmp localhost/sample -d -o /tmp```

Note: the '-d' flag means 'download latest' and '-o' is the volume mounted directory where 
the latest binary will be download.

## Sample Output

```yaml
$ docker run -it --privileged -v $(pwd):/tmp localhost/sample -d -o /tmp
Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
Discovered the latest version from the GitHub API: v2.213.2.
Downloading the latest binary from https://vstsagentpackage.azureedge.net/agent/2.213.2/vsts-agent-linux-x64-2.213.2.tar.gz
Binary saved as /tmp/vsts-agent-linux.tar.gz
```