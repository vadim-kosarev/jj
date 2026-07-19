# jj

Домашняя песочница: Docker-стек с Kafka/ClickHouse/Redis/Postgres/Langflow/Flowise + Java-демо (Spring Boot) + вспомогательные Python-скрипты.

## Быстрый старт (для ленивых)

```powershell
# 1. выбрать конфиг под текущий хост (один раз, или при смене машины)
Copy-Item .env.STARLIGHT .env -Force   # либо .env.BRIGHTSKY

# 2. внешняя сеть докера (если ещё не создана)
docker network create docker-network

# 3. поднять весь стек
docker compose up -d

# 4. глянуть логи конкретного сервиса
docker compose logs -f kafka1

# 5. погасить
docker compose down
```

Полная зачистка томов (**удаляет данные**, сверься с актуальными именами volume в `docker-compose.yml` — скрипт местами устарел):
```powershell
.\cleanup.cmd
```

## Сервисы

| Сервис       | Адрес                                                          | Что это                            |
| ------------ | -------------------------------------------------------------- | ----------------------------------- |
| Kafka        | `localhost:2160` (external), `kafka.rgzz:2161` (внутри сети)   | брокер, KRaft-режим, без Zookeeper  |
| Kafka UI     | http://localhost:8385                                          | веб-морда кафки                     |
| ClickHouse   | http://localhost:8123 (HTTP), `localhost:9000` (TCP)           | аналитическая БД                    |
| OTel Collector | `localhost:4317` (gRPC), `localhost:4318` (HTTP)             | приёмник трейсов/метрик/логов (OTLP), пока просто логирует их в debug-экспортёр |
| Redis        | `localhost:6379`                                               | кэш/стор                            |
| RedisInsight | http://localhost:5540                                          | веб-морда Redis                     |
| Postgres     | `localhost:5432`                                               | БД для Langflow и Flowise           |
| Langflow     | http://localhost:7860                                          | no-code LLM оркестратор             |
| Flowise      | http://localhost:3020                                          | no-code LLM оркестратор             |

Логины/пароли — смотри `.env` (см. ниже).

## Конфигурация и секреты

- `.env` — активный конфиг, в `.gitignore`, не коммитится.
- `.env.STARLIGHT` / `.env.BRIGHTSKY` — шаблоны под конкретные хосты, коммитятся в git, копируются в `.env`.
- Все пароли/ключи (Postgres, Langflow, Flowise, прокси) лежат в `.env*`, `docker-compose.yml` их только подставляет через `${VAR}`.

## Java-проект (`art`)

Spring Boot 4 / Java 21, лежит в `src/main/java/home/art`.

```powershell
.\gradlew.bat bootRun   # запустить
.\gradlew.bat build     # собрать
.\gradlew.bat test      # тесты
```

## Python-скрипты

`src/main/python` — генерация данных, пример Redis Cluster и т.п.:
```powershell
python src/main/python/generate_data.py
```

## Прочее

- `prepare_commit.py` — собирает `git status`/`diff` в `tmp/` для подготовки коммита.
- `docker/postgres/init.sql` — создаёт БД/юзеров `langflow` и `flowise` при первом старте контейнера postgres.