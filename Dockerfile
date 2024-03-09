FROM ubuntu:latest
LABEL authors="humanlearning"

ENTRYPOINT ["top", "-b"]