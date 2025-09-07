#!/bin/bash

echo "Installing dependencies..."

pip install -r requirements.txt
pip install groq==0.9.0
pip install cerebras_cloud_sdk==1.5.0

if [ -z "$GROQ_API_KEY" ]; then
  echo "GROQ_API_KEY environment variable is not set. Please set it to your project's GROQ API key. to use the groq provider."
fi

if [ -z "$CEREBRAS_API_KEY" ]; then
  echo "CEREBRAS_API_KEY environment variable is not set. Please set it to your project's CEREBRAS API key. to use the CEREBRAS provider."
fi

pip install httpx==0.28.1 --force-reinstall # Must be last to avoid conflicts with other dependencies

python string_ops/build.py

echo "Installation completed successfully!"