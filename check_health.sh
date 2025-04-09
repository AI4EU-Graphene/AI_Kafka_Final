#!/bin/bash

echo "Checking service health endpoints..."
ports=(5100 5101 5102 5103 5104 5105 5106 5110 5111 5107)

for port in "${ports[@]}"
do
  echo -n "Service at port $port: "
  curl -s http://localhost:$port/health || echo "Unavailable"
  echo ""
done