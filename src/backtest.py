from kafka_producer import KafkaProducer
from confluent_kafka import Consumer
from threading import Thread
import numpy as np
import json

KAFKA_SERVER = "broker:9092"
TOPIC = "mock_l1_stream"
ORDER_SIZE = 5000

class Venue:
	def __init__(self, Q=2000, rebate=0.002, fee=0.003): # Page 21 indicates these as typical parameters
		self.Q = Q # length of queue at each venue
		self.fee = fee # cost of market orders
		self.rebate = rebate # rebate for limit orders
		self.ask = None
		self.ask_size = None

class OrderAllocator:
	def __init__(self, venues: list[Venue]):
		self.params = { # use parameters from page 21 as baseline
			"h": 0.02, # exogenous spread - one half of bid/ask spread (using value from page 12)
			"theta": 0.0005, # marginal impact coefficient. (using value from page 12)
			"lam_u": 0.05, # delta under
			"lam_o": 0.05, # delta over
		}
		self.venues = venues
		self.executed = 0

	def allocate(self, S: int):
		chunk_size = 100 # search within 100 share chunks
		splits = [[]] # store order splits between venues
		for v in self.venues:
			new_splits = [] # process the venue and then overwrite `splits`
			for allocation in splits: # update each allocation in splits
				max_v = min(v.ask_size, S - sum(*splits))
				for q in range(0, max_v + 1, chunk_size):
					new_splits.append([max_v - max_v % 100])
			splits = new_splits
		print(f"Splits found as {splits}")

		best_cost = np.inf
		best_split = []
		for split_idx, allocation in enumerate(splits, 1):
			if sum([x[-1] for x in splits[:split_idx]]) != S:
				continue
			cost = self.compute_cost(S, allocation)
			if cost < best_cost:
				best_cost = cost
				best_split = allocation
		return best_split, best_cost

	def compute_cost(self, S, split):
		cash_spent = 0
		newly_executed = 0
		for sub_split, venue in zip(split, self.venues): # loop over each venue and how many shares were allocated to purchase there
			exe = min(sub_split, venue.ask_size)
			self.executed += exe
			cash_spent += exe * (venue.ask + venue.fee)
			maker_rebate = max(sub_split - exe, 0) * venue.rebate
			cash_spent -= maker_rebate

		underfill = max(S - newly_executed, 0)
		overfill = max(newly_executed - S, 0)
		risk_pen = self.params["theta"] * (underfill + overfill)
		cost_pen = self.params["lam_u"] * underfill + self.params["lam_o"] * overfill
		self.executed += newly_executed
		return cash_spent + risk_pen + cost_pen

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
	venue_list = [
		Venue() # Assuming l1_day.csv reflects one venue only. Use default venue parameters.
	]
	sor = OrderAllocator(venue_list) # smart order router
	kc = KafkaConsumer() # now we consume items as they are generated
	try:
		while True:
			msg = kc.consumer.poll(1.0)
			if msg is None:
				print("Waiting...")
			elif msg.error():
				print("ERROR: %s".format(msg.error()))
			else:
				data = json.loads(msg.value().decode('utf-8')) # Load update from Kafka, and convert to a dictionary
				venue_list[0].ask_size = int(data["ask_sz_00"]) # update our venue with current ask information
				venue_list[0].ask = float(data["ask_px_00"])
				print(f"Consumed event from topic {msg.topic()}: key = {msg.key().decode('utf-8'):12} value = {msg.value().decode('utf-8'):12}")
				print(f"allocation determined as: {sor.allocate(ORDER_SIZE)}")
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
