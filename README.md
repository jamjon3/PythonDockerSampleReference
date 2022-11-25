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

The python 
docker build --tag sample  .
docker run -it --privileged -v $(pwd):/tmp localhost/sample -d -o /tmp