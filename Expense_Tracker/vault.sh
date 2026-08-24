#!/bin/bash

# Exit on error
set -e

echo "Setting up HashiCorp Vault key-value secrets..."

export VAULT_ADDR="http://127.0.0.1:8200"
export VAULT_TOKEN="root"

until curl -s $VAULT_ADDR/v1/sys/health > /dev/null; do
  echo "Waiting for Vault server to start..."
  sleep 2
done

echo "Vault is reachable. Enabling KV secrets engine..."

docker exec -e VAULT_ADDR='http://127.0.0.1:8200' -e VAULT_TOKEN='root' vault_server vault secrets enable -path=secret kv-v2 || true

docker exec -e VAULT_ADDR='http://127.0.0.1:8200' -e VAULT_TOKEN='root' vault_server vault kv put secret/expense_tracker \
  DATABASE_URL="postgresql://postgres:postgrespassword@postgres_db:5432/expense_tracker" \
  SECRET_KEY="your-flask-secret-key"

echo "Vault initialization complete! Secrets have been written to secret/expense_tracker."
