#!/bin/bash

# Deployment script (deploy.sh)
# This script deploys Kubernetes resources in a serial order.

# Deploy ConfigMaps
echo "Deploying ConfigMaps..."
kubectl apply -f ../resources/configmaps/app-config.yaml

# Deploy PersistentVolumes and PersistentVolumeClaims
echo "Deploying PersistentVolumes and PersistentVolumeClaims..."
kubectl apply -f ../resources/pvs/mysql.yaml
kubectl apply -f ../resources/pvs/rabbitmq.yaml
kubectl apply -f ../resources/pvcs/mysql.yaml
kubectl apply -f ../resources/pvcs/rabbitmq.yaml

# Deploy Services
echo "Deploying Services..."
kubectl apply -f ../services/mysql/deployment.yaml
kubectl apply -f ../services/rabbitmq/deployment.yaml
kubectl apply -f ../services/redis/deployment.yaml
kubectl apply -f ../services/mysql/service.yaml
kubectl apply -f ../services/rabbitmq/service.yaml
kubectl apply -f ../services/redis/service.yaml

# Deploy Apps
echo "Deploying Apps..."
kubectl apply -f ../apps/server/deployment.yaml
kubectl apply -f ../apps/workers/deployment.yaml
kubectl apply -f ../apps/server/service.yaml

# Add more resource types and files as needed, following the same pattern.

echo "Deployment completed successfully."
