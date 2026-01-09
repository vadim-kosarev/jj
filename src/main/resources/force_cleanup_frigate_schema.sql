-- ============================================================================
-- FORCE CLEANUP SCRIPT: Remove all Frigate tables and replicas
-- Use this when regular cleanup fails with "Replica already exists"
-- ============================================================================

-- Force drop all replicas from ZooKeeper first
SYSTEM DROP REPLICA '01' FROM TABLE frigate.events_local_01;
SYSTEM DROP REPLICA '02' FROM TABLE frigate.events_local_01;
SYSTEM DROP REPLICA '01' FROM TABLE frigate.detection_summary_local_01;
SYSTEM DROP REPLICA '02' FROM TABLE frigate.detection_summary_local_01;
SYSTEM DROP REPLICA '01' FROM TABLE frigate.events_by_camera_local_01;
SYSTEM DROP REPLICA '02' FROM TABLE frigate.events_by_camera_local_01;
SYSTEM DROP REPLICA '01' FROM TABLE frigate.alert_events_local_01;
SYSTEM DROP REPLICA '02' FROM TABLE frigate.alert_events_local_01;

-- Wait a moment for ZooKeeper cleanup
SELECT sleep(2);

-- Now drop tables (they should drop cleanly now)
DROP VIEW IF EXISTS frigate.rabbitmq_error_to_table ON CLUSTER my_cluster;
DROP VIEW IF EXISTS frigate.rabbitmq_to_events ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.alert_events ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.events_by_camera ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.detection_summary ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.events ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.alert_events_local_01 ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.events_by_camera_local_01 ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.detection_summary_local_01 ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.events_local_01 ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.rabbitmq_error_consumer ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.rabbitmq_events_queue_01 ON CLUSTER my_cluster;
DROP TABLE IF EXISTS frigate.rabbitmq_errors ON CLUSTER my_cluster;

-- Drop database if needed
-- DROP DATABASE IF EXISTS frigate ON CLUSTER my_cluster;
