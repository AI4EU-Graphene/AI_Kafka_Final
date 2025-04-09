#!/bin/bash

DOCKER_USER=vaibhavtechie

services=(
  smart-ingestor
  smart-preprocessor
  smart-ml-preprocessor
  smart-model-trainer
  smart-ml-forecaster
  smart-anomaly-detector
  smart-alert-engine
  smart-grid-rebalancer
  smart-storage-optimizer
  ai-pipeline
)

for service in "${services[@]}"
do
  echo "🔨 Building $service..."
  docker build -t $DOCKER_USER/$service:latest ./$service
done

echo "✅ All services built locally. You can now push them via Docker Desktop or CLI."