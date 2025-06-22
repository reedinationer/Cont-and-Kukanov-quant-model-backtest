# Video walkthrough
https://youtu.be/TRjKZs3T9Uk

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
    docker logs pyscript --follow
    docker compose down

Rebuild command for debugging

    docker compose up -d --force-recreate --build pyscript

# Approach

We are only given the limit order book of a single venue.
Cont and Kukanov show with Proposition 3 that for a single venue the market order quantity will increase linearly.


# Tuning logic
