#!/bin/bash

# Start the Ollama server in the background
ollama serve &

# Wait until Ollama server is ready
until curl -s http://localhost:11434/version > /dev/null; do
  echo "Waiting for Ollama server to start..."
  sleep 1
done

echo "Ollama is up. Pulling tinyllama..."
ollama pull tinyllama:1b
echo "Pulling llama3.2..."
ollama pull llama3.2:1b
