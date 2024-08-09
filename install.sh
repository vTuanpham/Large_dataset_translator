#!/bin/bash

echo "Installing dependencies..."

pip install -r requirements.txt
pip install groq==0.9.0
pip install httpx==1.0.0.beta0 --force-reinstall

echo "Installation completed successfully!"