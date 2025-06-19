# sends l1_day.csv to Kafka


# - Parse `l1_day.csv` and create per-timestamp venue snapshots using:
#     - `publisher_id`, `ask_px_00`, `ask_sz_00`
# - Stream these snapshots via a Kafka producer to topic `mock_l1_stream`
# - Use `time.sleep()` or `ts_event` deltas to simulate real-time pacing
# - Use the time range `13:36:32` to `13:45:14 UTC` from the dataset as the window for your simulation and evaluation.


