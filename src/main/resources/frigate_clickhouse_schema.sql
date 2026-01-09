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

select * from frigate.q_frigate_events_raw FINAL;


