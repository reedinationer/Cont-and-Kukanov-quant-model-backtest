# EC2 Environment setup

First, generate a new AWS EC2 instance. This README implemented a Ubuntu OS, but the process should be similar for any linux EC2 instance.
Connect to the instance and start configuring the environment as so:

Get Docker on the EC2 instance

    sudo apt-get update
    sudo apt-get install ca-certificates curl gnupg
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    echo \
      "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

Check everything went correctly by running

    docker --version

Wrap up docker install with adjusting user permissions so docker can be run without sudo

    sudo usermod -aG docker $USER
    newgrp docker

Pull the Kafka image with 

    docker pull apache/kafka

Or alternatively, as described in the documentation https://hub.docker.com/r/apache/kafka,
a Kafka broker can be started with 

    docker run -d --name broker apache/kafka:latest

Next, start a shell inside the container so we can add a topic

    docker exec --workdir /opt/kafka/bin/ -it broker sh

We will create a topic "mock_l1_stream" within our Kafka broker

    ./kafka-topics.sh --bootstrap-server localhost:9092 --create --topic mock_l1_stream

Follow the steps outlined here to install Confluent
https://docs.confluent.io/confluent-cli/current/install.html

Start a Kafka broker as described here
https://developer.confluent.io/get-started/python/#kafka-setup
with the command

`confluent local kafka start`

Note the plaintext ports section of the output from the previous command.


| Kafka REST Port | 8082  |

| Plaintext Ports | 12612 |


Create a kafka topic called "mock_l1_stream" by following this command

`confluent local kafka topic create mock_l1_stream`

When done, close the session with

`confluent local kafka stop`

# Approach

# Tuning logic

# EC2 setup