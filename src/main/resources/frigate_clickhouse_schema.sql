-- frigate.rabbitmq_events definition

CREATE table if not EXISTS frigate.q_frigate_events_mq
(
    `message_body` String
)
    ENGINE = RabbitMQ
        SETTINGS rabbitmq_host_port = 'rabbitmq.rgzz:5672',
            rabbitmq_username = 'rgzz',
            rabbitmq_password = 'rgzz',
            rabbitmq_vhost = 'rgzz',
            rabbitmq_queue_base = 'q-frigate-events',
            rabbitmq_queue_consume = 1,
            rabbitmq_exchange_name = '',
            rabbitmq_format = 'JSONAsString',
            rabbitmq_num_consumers = 1,
            rabbitmq_skip_broken_messages = 1;


-- frigate.events_raw definition

CREATE TABLE if not exists frigate.q_frigate_events_raw
(
    `message_body` String,
    `ingested_at` DateTime DEFAULT now()
)
    ENGINE = MergeTree
        ORDER BY ingested_at
        SETTINGS index_granularity = 8192;


create materialized view if not exists frigate.q_frigate_event_mv
            to frigate.q_frigate_events_raw
as
select
    `message_body`
from frigate.q_frigate_events_mq;

