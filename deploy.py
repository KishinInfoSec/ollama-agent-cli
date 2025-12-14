#!/usr/bin/env python3
"""Deployment one-liner: python3 deploy.py"""

# Setup venv and deploy with model detection in one line
exec('import subprocess, sys, os, json; [subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True) if not os.path.exists(".venv") else None, (venv_python := os.path.join(".venv", "bin", "python")), subprocess.run([venv_python, "-m", "pip", "install", "-q", "-e", "."], check=True), (models := json.loads(subprocess.run(["ollama", "list", "--format", "json"], capture_output=True, text=True, check=False).stdout or "{}").get("models", [{}])), (selected := models[0]["name"] if models else "llama2"), print(f"✓ Deployment complete!\\n✓ Using model: {selected}\\n✓ Virtual env: {os.path.abspath(\".venv\")}\\n✓ Ready: {venv_python} -m ollama_agent.cli interactive --model {selected}"), subprocess.run([venv_python, "-m", "ollama_agent.cli", "check-connection", "--model", selected], check=False)][-1]')
