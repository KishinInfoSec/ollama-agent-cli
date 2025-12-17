# Quick Reference Card

## Ollama Cybersecurity Agent CLI - Command Cheat Sheet

### Installation (One-Time Setup)

```bash
# Automated setup (RECOMMENDED)
cd /path/to/dir
bash quick_start.sh

# OR manual setup
pip install -e .
```

### Prerequisites

```bash
# 1. Install Ollama (one-time)
# Download from https://ollama.ai

# 2. Start Ollama server (keep running in separate terminal)
ollama serve

# 3. Install a model (one-time)
ollama pull llama2      # Recommended
# OR
ollama pull mistral     # Faster alternative
```

---

## Essential Commands

### Connection & Setup

```bash
# Test Ollama connection
ollama-agent check-connection

# List installed models
ollama-agent check-connection  # Shows models

# List available prompt modes
ollama-agent list-modes
```

### Interactive Chat (Recommended for Learning)

```bash
# Start interactive chat (default mode)
ollama-agent interactive

# With specific model
ollama-agent interactive --model mistral

# With specific prompt mode
ollama-agent interactive --mode threat_analysis

# With temperature adjustment
ollama-agent interactive --temperature 0.5

# Combine options
ollama-agent interactive --model llama2 --mode compliance --temperature 0.6
```

### Single Queries (Quick Answers)

```bash
# Simple query
ollama-agent query "Your security question here"

# With specific mode
ollama-agent query "Your question" --mode vulnerability

# With specific model
ollama-agent query "Your question" --model mistral

# Combine options
ollama-agent query "Your question" --mode incident_response --temperature 0.5
```

---

## Prompt Modes (--mode)

Use `--mode` with any command to switch security domains:

| Mode | Best For |
|------|----------|
| `default` | General security questions |
| `threat_analysis` | Threat modeling, actor analysis |
| `incident_response` | Security incidents, forensics |
| `vulnerability` | CVEs, vulnerability fixes |
| `compliance` | Audits, standards (NIST, CIS, ISO) |
| `secure_coding` | Code review, development security |
| `network` | Network design, architecture |
| `malware` | Malware analysis, detection |

### Examples by Mode

```bash
# Threat Analysis
ollama-agent query "What are APT tactics?" --mode threat_analysis

# Incident Response
ollama-agent query "We have ransomware, what to do?" --mode incident_response

# Vulnerability
ollama-agent query "How serious is CVE-2024-1234?" --mode vulnerability

# Compliance
ollama-agent query "What's required for SOC 2?" --mode compliance

# Secure Coding
ollama-agent query "Is this code safe? [code]" --mode secure_coding

# Network
ollama-agent query "Design secure network" --mode network

# Malware
ollama-agent query "Analyze this behavior" --mode malware
```

---

## Interactive Mode Special Commands

Use these inside interactive mode (type and press Enter):

| Command | Purpose |
|---------|---------|
| `/help` | Show help message |
| `/modes` | List all prompt modes |
| `/models` | List installed Ollama models |
| `/tools` | Show available security tools |
| `/clear` | Clear conversation history |
| `/mode <name>` | Switch to different mode |
| `/exit` | Exit the agent |

### Interactive Mode Examples

```bash
# Start interactive
$ ollama-agent interactive

You: What are common web vulnerabilities?
Agent: The most common web vulnerabilities include...

You: /mode secure_coding
(Switched to secure_coding mode)

You: Show me how to prevent these in code
Agent: To prevent common vulnerabilities in code...

You: /clear
(Conversation cleared)

You: /exit
```

---

## Temperature Settings (--temperature)

Adjust model behavior with `--temperature` (0.0 to 1.0):

```bash
# Technical/Precise responses (use 0.3-0.5)
ollama-agent query "Define zero-day" --temperature 0.3

# Balanced responses (use 0.6-0.7) - RECOMMENDED
ollama-agent query "Analyze this threat" --temperature 0.7

# Creative/Varied responses (use 0.8-1.0)
ollama-agent query "Brainstorm security ideas" --temperature 0.9
```

---

## Model Selection

```bash
# Fast/Small (7B parameters) - Recommended for learning
ollama pull mistral       # Fastest
ollama pull neural-chat   # Good for chat

# Balanced (7B) - Good quality
ollama pull llama2        # Recommended
ollama pull dolphin-mixtral  # High quality

# Large/Slow (13B+) - Best quality but slower
ollama pull llama2-13b    # Higher quality
ollama pull mixtral-8x7b  # Very capable but large

# Use with CLI
ollama-agent interactive --model mistral
ollama-agent query "..." --model llama2-13b
```

---

## Real-World Examples

### Quick Security Check
```bash
ollama-agent query "What are the top security risks for my web app?"
```

### Threat Analysis Session
```bash
ollama-agent interactive --mode threat_analysis
# Then ask about specific threat actors, attack vectors, etc.
```

### Incident Response
```bash
ollama-agent query "We detected suspicious activity. Steps?" --mode incident_response
```

### Compliance Prep
```bash
ollama-agent query "Preparing for HIPAA audit. Checklist?" --mode compliance
```

### Code Security Review
```bash
# Cat a file and pipe to agent
cat my_app.py | xargs -0 -I {} ollama-agent query \
  "Review this code for security issues: {}" --mode secure_coding
```

### Batch Analysis Report
```bash
#!/bin/bash
echo "=== Security Assessment ==="

echo "1. Threat Analysis"
ollama-agent query "Current threat landscape?" --mode threat_analysis

echo "2. Vulnerability Review"
ollama-agent query "Critical vulnerabilities?" --mode vulnerability

echo "3. Compliance Status"
ollama-agent query "Compliance gaps?" --mode compliance
```

---

## Troubleshooting Quick Fixes

### Problem: Connection Error
```bash
# Make sure Ollama is running
ollama serve  # In another terminal

# Then try
ollama-agent check-connection
```

### Problem: Model Not Found
```bash
# List available models
ollama list

# Install a model
ollama pull llama2
```

### Problem: Slow Responses
```bash
# Use faster model
ollama pull mistral
ollama-agent interactive --model mistral

# OR reduce temperature
ollama-agent interactive --temperature 0.3
```

### Problem: Different Ollama Port
```bash
ollama-agent check-connection --host http://localhost:11435
ollama-agent interactive --host http://localhost:11435
```

---

## Documentation Quick Links

| Need | Read |
|------|------|
| Getting started | `GETTING_STARTED.md` |
| Full reference | `README.md` |
| Real examples | `EXAMPLES.md` |
| Technical details | `ARCHITECTURE.md` |
| Development | `CONTRIBUTING.md` |
| Navigation | `INDEX.md` |

---

## Common Workflows

### Workflow 1: Daily Security Check (5 minutes)
```bash
ollama-agent query "Summary of security best practices"
```

### Workflow 2: Incident Analysis (15 minutes)
```bash
ollama-agent interactive --mode incident_response
# Ask detailed questions about the incident
```

### Workflow 3: Compliance Audit (30 minutes)
```bash
ollama-agent interactive --mode compliance
# Work through audit requirements
```

### Workflow 4: Code Review (10 minutes)
```bash
ollama-agent query "Review for security: [paste code]" --mode secure_coding
```

---

## Performance Tips

```bash
# Fastest: Small model + low temperature
ollama-agent interactive --model mistral --temperature 0.3

# Balanced: Medium model + medium temperature (RECOMMENDED)
ollama-agent interactive --model llama2 --temperature 0.7

# Best Quality: Large model + medium-high temperature
ollama-agent interactive --model llama2-13b --temperature 0.8
```

---

## Environment Setup (Optional)

```bash
# Set default model
export OLLAMA_MODEL=mistral

# Set default host
export OLLAMA_HOST=http://localhost:11434

# Then use without specifying:
ollama-agent interactive
```

---

## Help & Version

```bash
# Show help
ollama-agent --help

# Show command help
ollama-agent interactive --help
ollama-agent query --help
ollama-agent check-connection --help
```

---

## Installation Verification

```bash
# Check installation
which ollama-agent
ollama-agent --help

# Test Ollama
ollama-agent check-connection

# Try first query
ollama-agent query "Hello"
```

---

## Next Steps

1. **Start**: `ollama serve` (in one terminal)
2. **Test**: `ollama-agent check-connection`
3. **Try**: `ollama-agent interactive`
4. **Learn**: Read `README.md`
5. **Explore**: Try different modes with `/mode`

---

**Tip:** Save this file and refer back to it!

**Command History:**
```bash
# Copy & paste this to quickly try the agent:
ollama-agent interactive --temperature 0.7
```

---

*Version: 0.1.0*
*Last Updated: 2024*
