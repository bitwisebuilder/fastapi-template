#!/bin/bash

# Sub-script to validate configmaps (validate_configmaps.sh)

# Loop through ConfigMap YAML files in the 'resources/configmaps' folder
for file in ../resources/configmaps/app-config.yaml; do
  echo "Validating $file"
  kubectl apply --dry-run=client -f "$file"
  if [ $? -ne 0 ]; then
    echo "Error: Validation failed for $file"
    exit 1
  fi
done
