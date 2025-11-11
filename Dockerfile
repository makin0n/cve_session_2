FROM buildpack-deps:stable-scm

WORKDIR /app

COPY . /app

CMD ["/bin/bash"]