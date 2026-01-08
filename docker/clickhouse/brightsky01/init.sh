#!/bin/bash

clickhouse-client --user clickhouse --password clickhouse --database default -q "CREATE DATABASE IF NOT EXISTS aabb;"
