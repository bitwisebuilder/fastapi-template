#!/bin/bash

# Sub-script to validate services (validate_services.sh)

# Loop through service YAML files in the 'apps' and 'services' folders
for file in ../apps/server/service.yaml ../services/mysql/service.yaml ../services/rabbitmq/service.yaml ../services/redis/service.yaml; do
  echo "Validating $file"
  kubectl apply --dry-run=client -f "$file"
  if [ $? -ne 0 ]; then
    echo "Error: Validation failed for $file"
    exit 1
  fi
done
