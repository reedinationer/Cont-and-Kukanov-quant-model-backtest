from kafka_producer import KafkaProducer
from confluent_kafka import Consumer
from threading import Thread

KAFKA_SERVER = "broker:9092"
TOPIC = "mock_l1_stream"
CSV_FILE = "reference/l1_day.csv"

import csv
with open(CSV_FILE, "r") as csv_file:
	reader = csv.DictReader(csv_file)
	for row in reader:
		print(row)
		break

class Venue:
	def __init__(self, Qk: int, rk: float):
		self.Qk = Qk # length of queue at each venue
		self.rk = rk # rebate of this venue

class OrderAllocator:
	def __init__(self, venues):
		self.params = { # use parameters from page 21 as baseline
			"f": 0.003,
			"h": 0.02,
			"theta": 0.0005,
			"del_u": 0.05, # delta under
			"del_o": 0.05, # delta over
			"K": len(venues), # number of venues
		}
		self.venues = venues

	def allocate(self, S: int):
		chunk_size = 100 # optimize orders within 100 share chunks
		splits = [] # store order splits
		for v in self.venues:
			new_splits = []
			for allocation in splits:
				used = sum(all)


	def allocate(self, order_size, venues, λ_over, λ_under, θ_queue):
	step        ← 100  # search in 100-share chunks
	splits      ← [[]]  # start with an empty allocation list
	for v in 0..len(venues) - 1:
		new_splits ← []
		for alloc in splits:
			used ← sum(alloc)
			max_v ← min(order_size - used, venues[v].ask_size)
			for q in 0..max_v step step:
				new_splits.append(alloc + [q])
		splits ← new_splits

	best_cost  ← +∞
	best_split ← []
	for alloc in splits:
		if sum(alloc) ≠ order_size: continue
		cost ← compute_cost(alloc, venues,
		                    order_size, λ_over, λ_under, θ_queue)
		if cost < best_cost:
			best_cost  ← cost
			best_split ← alloc
	return best_split, best_cost

# Consumes stream, applies allocator logic
class KafkaConsumer:
	def __init__(self):
		self.config = {
			# User-specific properties that you must set
        'bootstrap.servers': f'{KAFKA_SERVER}',

        # Fixed properties
        'group.id':          'kafka-python-getting-started',
        'auto.offset.reset': 'earliest'
		}
		self.consumer = Consumer(self.config)
		self.consumer.subscribe([TOPIC])

def producer_func():
	producer = KafkaProducer()
	return producer

if __name__ == "__main__":
	t = Thread(target=producer_func) # Make a process to generate items into Kafka
	t.start()
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
	t.join()
	"""Final stdout must print a valid JSON like the format below:
	{
	  "best_parameters": {...},
	  "optimized": {...},
	  "baselines": {...},
	  "savings_vs_baselines_bps": {...}
	}"""
