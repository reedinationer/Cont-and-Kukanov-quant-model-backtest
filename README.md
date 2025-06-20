# Environment setup
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