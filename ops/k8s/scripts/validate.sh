#!/bin/bash

# Main validation script (validate.sh)
# This script orchestrates the validation process.

# Validate Deployments
bash validate_deployments.sh

# Validate Services
bash validate_services.sh

# Validate ConfigMaps
bash validate_configmaps.sh
