import time
import random
from datetime import datetime, timedelta
from clickhouse_connect import Client

client = Client(host="clickhouse-starlight-01", port=8123, database="default")
# jdbc:clickhouse://clickhouse-starlight-01:8123

ROWS = 1_000_000
TENANTS = 1000
START_TS = datetime.now() - timedelta(days=30)

tables = [
    "merge_tree",
    "replacing_merge_tree",
    "collapsing_merge_tree",
    "summing_merge_tree",
]

def generate_rows():
    rows = []
    for i in range(ROWS):
        tenant_id = random.randint(1, TENANTS)
        event_id = i
        ts = START_TS + timedelta(seconds=random.randint(0, 2_000_000))
        value = random.randint(1, 100)
        sign = random.choice([1, -1])
        version = random.randint(1, 10)
        rows.append((tenant_id, event_id, ts, value, sign, version))
    return rows

data = generate_rows()

for table in tables:
    client.execute(f"TRUNCATE TABLE perf.{table}")

for table in tables:
    start = time.time()
    client.execute(
        f"INSERT INTO perf.{table} VALUES",
        data
    )
    elapsed = time.time() - start
    print(f"{table}: insert time = {elapsed:.2f}s")
