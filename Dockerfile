FROM ubuntu:18.04

WORKDIR /ei

# Install base dependencies
RUN apt update && apt install -y build-essential software-properties-common wget

# Install LLVM 9
RUN wget https://apt.llvm.org/llvm.sh && chmod +x llvm.sh && ./llvm.sh 9
RUN rm /usr/bin/gcc && rm /usr/bin/g++ && ln -s $(which clang-9) /usr/bin/gcc && ln -s $(which clang++-9) /usr/bin/g++

# Install Python 3.7
RUN add-apt-repository ppa:deadsnakes/ppa && apt install -y python3.7

# Copy the base application in
COPY app ./app

# Copy any scripts in that we have
COPY *.py ./

# This is the script our application should run (-u to disable buffering)
ENTRYPOINT [ "python3", "-u", "build.py" ]