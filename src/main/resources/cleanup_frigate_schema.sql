-- ============================================================================
-- CLEANUP SCRIPT: Remove all Frigate tables and database
-- Execute this script before running the schema creation script
-- ============================================================================

-- Drop materialized views first (dependencies)
DROP VIEW IF EXISTS frigate.rabbitmq_error_to_table ON CLUSTER my_cluster;
DROP VIEW IF EXISTS frigate.rabbitmq_to_events ON CLUSTER my_cluster;

-- Drop distributed tables
DROP TABLE IF EXISTS frigate.alert_events ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.events_by_camera ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.detection_summary ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.events ON CLUSTER my_cluster;

-- Drop local tables
DROP TABLE IF EXISTS frigate.alert_events_local_01 ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.events_by_camera_local_01 ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.detection_summary_local_01 ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.events_local_01 ON CLUSTER my_cluster;

-- Drop RabbitMQ tables
DROP TABLE IF EXISTS frigate.rabbitmq_error_consumer ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.rabbitmq_events_queue_01 ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.rabbitmq_errors ON CLUSTER my_cluster;

-- Force drop replicas from ZooKeeper (if tables still exist)
SYSTEM DROP REPLICA '01' FROM TABLE frigate.events_local;
SYSTEM DROP REPLICA '02' FROM TABLE frigate.events_local;
SYSTEM DROP REPLICA '01' FROM TABLE frigate.detection_summary_local;
SYSTEM DROP REPLICA '02' FROM TABLE frigate.detection_summary_local;
SYSTEM DROP REPLICA '01' FROM TABLE frigate.events_by_camera_local;
SYSTEM DROP REPLICA '02' FROM TABLE frigate.events_by_camera_local;
SYSTEM DROP REPLICA '01' FROM TABLE frigate.alert_events_local;
SYSTEM DROP REPLICA '02' FROM TABLE frigate.alert_events_local;

-- Drop database (optional - uncomment if you want to remove everything)
-- DROP DATABASE IF EXISTS frigate ON CLUSTER my_cluster;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Check if tables are removed
-- SELECT database, name, engine FROM system.tables WHERE database = 'frigate';

-- Check if replicas are cleaned up
-- SELECT database, table, replica_name FROM system.replicas WHERE database = 'frigate';

-- Check ZooKeeper paths (should be empty after cleanup)
-- SELECT * FROM system.zookeeper WHERE path LIKE '/clickhouse/tables/frigate%';
