# ClickHouse Setup

## Connection to Main ClickHouse

To connect to the ClickHouse cluster, use one of the nodes:

- **STARLIGHT Node**: `http://clickhouse.starlight:8123` (HTTP) or `clickhouse.starlight:9000` (TCP)
- **BRIGHTSKY Node**: `http://clickhouse.brightsky:8124` (HTTP) or `clickhouse.brightsky:9001` (TCP)

For distributed queries, create distributed tables pointing to the `my_cluster` cluster.

Example connection using clickhouse-client:
```
clickhouse-client --host clickhouse.starlight --port 9000 --user default --password password123
```

Or via HTTP:
```
curl 'http://clickhouse.starlight:8123/?query=SELECT%201'
```

The cluster is configured for sharding and replication across the two nodes.
