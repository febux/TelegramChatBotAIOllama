#!/bin/bash

./bin/ollama serve &

pid=$!

echo "Model: $1"
model=$1

sleep 5


echo "Pulling model $model..."
ollama pull $model


wait $pid