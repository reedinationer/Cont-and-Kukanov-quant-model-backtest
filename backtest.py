from kafka_producer import * #

# Consumes stream, applies allocator logic


if __name__ == "__main__":
	"""Final stdout must print a valid JSON like the format below:
	{
	  "best_parameters": {...},
	  "optimized": {...},
	  "baselines": {...},
	  "savings_vs_baselines_bps": {...}
	}"""
