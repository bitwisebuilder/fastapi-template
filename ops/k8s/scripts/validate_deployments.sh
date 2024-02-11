#!/bin/bash

# Sub-script to validate deployments (validate_deployments.sh)

# Loop through deployment YAML files in the 'apps' folder
for file in ../apps/server/deployment.yaml ../apps/workers/deployment.yaml; do
  echo "Validating $file"
  kubectl apply --dry-run=client -f "$file"
  if [ $? -ne 0 ]; then
    echo "Error: Validation failed for $file"
    exit 1
  fi
done
