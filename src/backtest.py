from src.kafka_producer import KafkaProducer
import confluent_kafka
from threading import Thread


PLAINTEXT_PORTS = 9092
TOPIC = "mock_l1_stream"

# Consumes stream, applies allocator logic
class KafkaConsumer:
	def __init__(self):
		self.config = {
			# User-specific properties that you must set
        'bootstrap.servers': f'localhost:{PLAINTEXT_PORTS}',

        # Fixed properties
        'group.id':          'kafka-python-getting-started',
        'auto.offset.reset': 'earliest'
		}
		self.consumer = confluent_kafka.Consumer(self.config)
		self.consumer.subscribe([TOPIC])

def producer_func():
	producer = KafkaProducer()

if __name__ == "__main__":
	p = Thread(target=producer_func) # Make a process to generate items into Kafka
	kc = KafkaConsumer() # now we consume items as they are generated
	try:
		while True:
			msg = kc.consumer.poll(1.0)
			if msg is None:
				# Initial message consumption may take up to
				# `session.timeout.ms` for the consumer group to
				# rebalance and start consuming
				print("Waiting...")
			elif msg.error():
				print("ERROR: %s".format(msg.error()))
			else:
				# Extract the (optional) key and value, and print.
				print(f"Consumed event from topic {msg.topic()}: key = {msg.key().decode('utf-8'):12} value = {msg.value().decode('utf-8'):12}")
	except KeyboardInterrupt:
		pass
	finally:
		# Leave group and commit final offsets
		kc.consumer.close()
	"""Final stdout must print a valid JSON like the format below:
	{
	  "best_parameters": {...},
	  "optimized": {...},
	  "baselines": {...},
	  "savings_vs_baselines_bps": {...}
	}"""
