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

Pull the Kafka image as described in the documentation https://hub.docker.com/r/apache/kafka.
A Kafka broker can be started with 

    docker run -d --name broker apache/kafka:latest

Next, start a shell inside the container so we can add a topic

    docker exec --workdir /opt/kafka/bin/ -it broker sh

We will create the topic "mock_l1_stream" within our Kafka broker

    ./kafka-topics.sh --bootstrap-server localhost:9092 --create --topic mock_l1_stream

Now we install git and pull the repository

    sudo apt install git
    cd ~
    mkdir QuantModel
    cd QuantModel/
    git init
    git remote add origin https://github.com/reedinationer/Cont-and-Kukanov-quant-model-backtest.git
    git branch --set-upstream-to=origin/main master
    git pull

Now use docker to build and run the multi container application

    docker compose build --with-dependencies    
    docker compose up -d
    docker logs init
    docker logs broker
    docker logs pyscript --follow
    docker compose down -v


# Approach

# Tuning logic
