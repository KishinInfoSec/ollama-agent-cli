#!/bin/bash
# Quick start script for Ollama Cybersecurity Agent CLI

set -e

# ASCII Art Banner
cat << "EOF"
  ___  _     _     _    __  __   _  
 / _ \| |   | |   / \  |  \/  | / \ 
| | | | |   | |  / _ \ | |\/| |/ _ \
| |_| | |___| | / ___ \| |  | / ___ \
 \___/|_____|_|/_/   \_\_|  |_/_/   \_\
                                       
    Cybersecurity Agent CLI
        Quick Start Setup
EOF

echo ""
echo "================================"
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Please install it from https://ollama.ai"
    exit 1
fi

echo "✓ Ollama found"

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama server is not running"
    echo "Start it with: ollama serve"
    echo ""
else
    echo "✓ Ollama server is running"
fi

# Install the CLI tool
echo ""
echo "Installing Ollama Cybersecurity Agent CLI..."
cd "$(dirname "$0")"
pip install -e . --quiet

if [ $? -eq 0 ]; then
    echo "✓ Installation successful!"
else
    echo "❌ Installation failed"
    exit 1
fi

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Start Ollama (if not already running):"
echo "   ollama serve"
echo ""
echo "2. Pull a model (if not already installed):"
echo "   ollama pull llama2"
echo ""
echo "3. Test the connection:"
echo "   ollama-agent check-connection"
echo ""
echo "4. Start interactive chat:"
echo "   ollama-agent interactive"
echo ""
echo "5. Or send a single query:"
echo "   ollama-agent query 'What are the top cybersecurity threats?'"
echo ""
echo "For more information:"
echo "   ollama-agent --help"
echo "   cat README.md"
echo ""
