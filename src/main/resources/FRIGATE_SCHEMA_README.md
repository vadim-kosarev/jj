# ClickHouse Schema для Frigate Events из RabbitMQ

## Описание

Простая схема для получения и хранения событий Frigate из RabbitMQ в виде сырого JSON.

**Параметры подключения:**
- **RabbitMQ URL**: `amqp://rgzz:rgzz@rabbitmq.rgzz:5672/rgzz`
- **Queue**: `q-frigate-events`
- **Кластер**: my_cluster (4 узла)

## Таблицы

### 1. `frigate.rabbitmq_events` - RabbitMQ Consumer
Получает сообщения из очереди и хранит сырой JSON.

### 2. `frigate.events_raw` - Хранение событий
Хранит все события с метаданными и полным JSON.

### 3. `frigate.events` - Distributed таблица
Для запросов ко всем событиям кластера.

## Развертывание

```bash
# Выполнить скрипт создания таблиц
clickhouse-client -h localhost -p 9000 -u clickhouse --password clickhouse < frigate_clickhouse_schema.sql
```

## Просмотр событий

```sql
-- Все события
SELECT timestamp, camera, event_id, event_type, raw_json
FROM frigate.events
ORDER BY timestamp DESC
LIMIT 10;

-- События по камере
SELECT timestamp, event_id, raw_json
FROM frigate.events
WHERE camera = 'cam1'
ORDER BY timestamp DESC;
```

