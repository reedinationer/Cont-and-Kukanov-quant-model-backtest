import confluent_kafka
import csv
import datetime
import time
import json

"""This file process the data in l1_day.csv and sends it to the Kafka topic mock_l1_stream"""

PLAINTEXT_PORTS = 9092
TOPIC = "mock_l1_stream"
CSV_FILE = "../l1_day.csv"
# Use the time range `13:36:32` to `13:45:14 UTC` from the dataset as the window for your simulation and evaluation.
MIN_TIME = datetime.time(hour=13, minute=36, second=32)
MAX_TIME = datetime.time(hour=13, minute=45, second=14, microsecond=999999)

def parse_timestamp(date_str):
	return datetime.datetime.strptime(date_str[:-4], "%Y-%m-%dT%H:%M:%S.%f")

def delivery_callback(err, msg):
	# per-message delivery callback to print the status once the message was either successful or failed permanently
	if err:
		print('ERROR: Message failed delivery: {}'.format(err))
	else:
		print(f"Produced event to topic {msg.topic()}: key = {msg.key().decode('utf-8'):12} value = {msg.value().decode('utf-8'):12}")


class KafkaProducer:
	def __init__(self):
		self.config = {
	        'bootstrap.servers': f'localhost:{PLAINTEXT_PORTS}',
	        'acks': 'all' # Make sure all followers acknowledge for maximum redundancy
        }
		self.producer = confluent_kafka.Producer(self.config)
		print(f"Parsing file {CSV_FILE}")
		with open(CSV_FILE, "r") as csv_file:
			reader = csv.DictReader(csv_file)
			t = None # Initialize time a null, and set it during the first loop
			for row in reader:
				# First, simulate real-time pacing using deltas of ts_event
				if t is None:
					t = parse_timestamp(row["ts_event"])
				else:
					new_time = parse_timestamp(row["ts_event"])
					delay = new_time - t
					time.sleep(delay.microseconds / 1000000.0) # convert to seconds when calling time.sleep
					t = new_time
				if MIN_TIME <= t.time() <= MAX_TIME: # only process orders during specified time
					# print(row)
					data = {
						"publisher_id": row["publisher_id"],
						"ask_px_00": row["ask_px_00"],
						"ask_sz_00": row["ask_sz_00"]
					}
					self.producer.produce(TOPIC, value=json.dumps(data), key=row["sequence"], partition=0, on_delivery=delivery_callback)
					self.producer.poll(1)
					self.producer.flush()
					pass # Now parse l1_day rows into snapshots using `publisher_id`, `ask_px_00`, `ask_sz_00`
				else:
					print(f"bad time: {row}")

		# Block until the messages are sent.
		# self.producer.poll(10000)
		# self.producer.flush()


if __name__ == '__main__':
	p = KafkaProducer()

