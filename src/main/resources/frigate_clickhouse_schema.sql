create database if not exists frigate;
use frigate;

-- frigate.rabbitmq_events definition

CREATE table if not EXISTS frigate.q_frigate_events_mq
(
    `message_body` JSON
)
    ENGINE = RabbitMQ
        SETTINGS rabbitmq_address = 'amqp://rgzz:rgzz@rabbitmq.rgzz:5672/rgzz',
            rabbitmq_queue_base = 'q-frigate-events',
            rabbitmq_queue_consume = 1,
            rabbitmq_exchange_name = '',
            rabbitmq_format = 'JSONAsObject',
            rabbitmq_num_consumers = 1,
            rabbitmq_skip_broken_messages = 0;


CREATE TABLE IF NOT EXISTS frigate.q_frigate_events_raw
(
    `message_hash` FixedString(32),
    `message_body` JSON,
    `ingested_at`  DateTime DEFAULT now()
)
    ENGINE = ReplacingMergeTree()
        ORDER BY (message_hash);
-- для дедупликации с приоритетом свежей записи

-- MV
CREATE MATERIALIZED VIEW if not exists frigate.q_frigate_event_mv
            to frigate.q_frigate_events_raw
AS
SELECT lower(hex(sipHash128(message_body))) AS message_hash, -- или MD5(message_body)
       message_body,
       now()                    AS ingested_at
FROM frigate.q_frigate_events_mq;



OPTIMIZE TABLE frigate.q_frigate_events_raw FINAL;


-- Denormalized table for analytical queries
CREATE TABLE IF NOT EXISTS frigate.q_frigate_events_denorm
(
    `event_type` String,
    `event_id` String,
    `camera` String,
    `label` String,
    `score` Float32,
    `active` Boolean,
    `box_x1` Int32,
    `box_y1` Int32,
    `box_x2` Int32,
    `box_y2` Int32,
    `area` Int32,
    `start_time` DateTime,
    `frame_time` DateTime,
    `top_score` Float32,
    `velocity_angle` Float32,
    `speed` Float32,
    `license_plate` Nullable(String),
    `path_points_count` Int32,
    `message_hash` FixedString(32),
    `ingested_at` DateTime DEFAULT now()
)
    ENGINE = ReplacingMergeTree()
        ORDER BY (camera, start_time);


-- Materialized View for automatic JSON decomposition from raw events
CREATE MATERIALIZED VIEW IF NOT EXISTS frigate.q_frigate_events_denorm_mv
            TO frigate.q_frigate_events_denorm
AS
SELECT
    message_body.type as event_type,
    message_body.after.id AS event_id,
    message_body.after.camera AS camera,
    message_body.after.label AS label,
    message_body.after.score AS score,
    message_body.after.active AS active,
    message_body.after.box[1] AS box_x1,
    message_body.after.box[2] AS box_y1,
    message_body.after.box[3] AS box_x2,
    message_body.after.box[4] AS box_y2,
    message_body.after.area AS area,
    toDateTime(message_body.after.start_time) AS start_time,
    toDateTime(message_body.after.frame_time) AS frame_time,
    message_body.after.top_score AS top_score,
    message_body.after.velocity_angle AS velocity_angle,
    message_body.after.current_estimated_speed AS speed,
    message_body.after.recognized_license_plate AS license_plate,
    length(message_body.after.path_data) AS path_points_count,
    message_hash,
    ingested_at
FROM frigate.q_frigate_events_raw
;

-- Example queries for analytics
-- SELECT * FROM frigate.q_frigate_events_denorm ORDER BY ingested_at DESC LIMIT 10;
-- SELECT camera, label, COUNT() as count, AVG(score) as avg_score FROM frigate.q_frigate_events_denorm GROUP BY camera, label ORDER BY count DESC;
-- SELECT camera, COUNT(DISTINCT event_id) as unique_events FROM frigate.q_frigate_events_denorm WHERE start_time > now() - INTERVAL 1 HOUR GROUP BY camera;
