#!/bin/bash
set -e

host="$1"
port="${2:-3306}"

echo "Waiting for MySQL at $host:$port..."

while ! nc -z "$host" "$port"; do
  sleep 3
done

echo "MySQL is up - executing command"
exec "${@:3}"
