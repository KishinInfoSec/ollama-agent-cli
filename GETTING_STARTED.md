# Getting Started with Ollama Cybersecurity Agent CLI

## What is This?

A powerful command-line tool that lets you interact with Ollama models (running locally on your machine) as an expert cybersecurity agent. It has 8 specialized prompt modes for different security analysis tasks.

**Key Benefits:**
- 🔒 All data stays on your machine (no cloud)
- 💬 Multi-turn conversations with context awareness
- 🎯 8 specialized prompt modes for different security domains
- 🛠️ Built-in security analysis tools
- ⚡ Real-time streaming responses

## Step 1: Install Ollama

1. Go to https://ollama.com
2. Download and install for your operating system
3. The installer will set up everything needed

## Step 2: Start Ollama Server

Open a terminal and run:
```bash
ollama serve
```

You should see output like:
```
2024-01-15 10:30:00 listening on 127.0.0.1:11434
```

Keep this terminal open while using the agent.

## Step 3: Pull a Model

Open a **new terminal** (keep the Ollama server running in the first one) and run:

```bash
# Option 1: Recommended for cybersecurity (good quality)
ollama pull llama2

# Option 2: Faster but smaller
ollama pull mistral

# Option 3: Optimized for chat
ollama pull neural-chat
```

This downloads the model (~4-7 GB depending on choice). First pull will take a few minutes.

## Step 4: Install the CLI Tool

```bash
cd /path/to/dir

# Automated setup
bash quick_start.sh

# OR manual installation
pip install -e .
```

## Step 5: Verify Installation

```bash
ollama-agent check-connection
```

You should see:
```
✓ Connected to Ollama
Host: http://localhost:11434
Available models: 1
  • llama2
```

## Step 6: Start Using It!

### Option A: Interactive Chat (Recommended for Learning)

```bash
ollama-agent interactive
```

Then type your cybersecurity questions. Example:
```
You: What are the main security risks of exposed S3 buckets?

Agent: Exposed S3 buckets pose several critical security risks...

You: How can I detect if my buckets are exposed?

Agent: There are several ways to detect exposed S3 buckets...

You: /mode incident_response
You: What would be the incident response steps?

Agent: Following an incident response framework...

You: /exit
```

### Option B: Single Query

```bash
ollama-agent query "Explain the OWASP Top 10 web vulnerabilities"
```

### Option C: Switch Analysis Modes

Each mode specializes in different security domains:

```bash
# Threat Analysis
ollama-agent interactive --mode threat_analysis

# Incident Response
ollama-agent query "What do I do if ransomware hits?" --mode incident_response

# Vulnerability Assessment
ollama-agent query "How serious is this CVE?" --mode vulnerability

# Compliance
ollama-agent query "What's required for HIPAA?" --mode compliance

# Secure Coding
ollama-agent query "Is this code secure? [code]" --mode secure_coding

# Network Security
ollama-agent query "How to design a secure network?" --mode network
```

## Common Interactive Commands

Inside interactive mode, use these special commands:

```
/help      - Show help
/modes     - List available modes
/models    - List installed Ollama models
/tools     - Show security tools info
/clear     - Clear conversation history
/mode <name> - Switch to different mode
/exit      - Exit
```

## Troubleshooting

### "Cannot connect to Ollama"

**Problem:** You get a connection error

**Solution:**
1. Make sure `ollama serve` is running in another terminal
2. Check it's on port 11434: `curl http://localhost:11434/api/tags`
3. If on different port, use: `ollama-agent check-connection --host http://localhost:11435`

### Model Not Found

**Problem:** Error about model not existing

**Solution:**
```bash
# See what models are installed
ollama list

# Install a model
ollama pull llama2
```

### Slow Responses

**Problem:** Responses are very slow

**Solution:**
- Use a faster model: `ollama pull mistral` or `ollama pull neural-chat`
- Reduce temperature: `ollama-agent interactive --temperature 0.3`
- Check if GPU is being used: `ollama ps`
- Ensure sufficient RAM is available

### "pip: command not found"

**Problem:** pip is not installed

**Solution:**
```bash
# Install Python 3.10+
python3 --version

# Use Python's pip module
python3 -m pip install -e .
```

## Real-World Examples

### Example 1: Security Audit Planning

```bash
$ ollama-agent query "Help me plan a security audit for a web application" --mode compliance
```

### Example 2: Incident Analysis

```bash
$ ollama-agent interactive --mode incident_response
You: We found suspicious SSH connections from unknown IPs
Agent: This indicates a potential unauthorized access attempt...
You: What should we do immediately?
Agent: Immediate actions: 1) Isolate affected systems...
```

### Example 3: Code Review

```bash
$ ollama-agent query "Review this code for security issues: $(cat my_app.py)" --mode secure_coding
```

### Example 4: Threat Analysis

```bash
$ ollama-agent interactive --mode threat_analysis
You: What's the threat profile for APIs?
Agent: APIs face several critical threats...
You: How do we defend against API attacks?
Agent: API security involves...
```

## Tips for Best Results

1. **Be Specific**: Instead of "How to be secure?" try "How to secure an AWS S3 bucket?"

2. **Provide Context**: "We have a Linux web server running Apache with MySQL backend" gives better results than "How to secure our server?"

3. **Use Appropriate Mode**: Use "incident_response" mode for breach questions, "compliance" for audit questions, etc.

4. **Adjust Temperature**:
   - Technical questions: `--temperature 0.3` (more focused)
   - Creative ideas: `--temperature 0.8` (more varied)

5. **Keep Context**: In interactive mode, conversations build on each other, so provide background early

## Next Steps

1. **Read the Full README**: `cat README.md` for comprehensive documentation
2. **Check Examples**: `cat EXAMPLES.md` for real security queries
3. **Explore Architecture**: `cat ARCHITECTURE.md` to understand how it works
4. **Customize Prompts**: Edit `src/ollama_agent/prompts.py` to add your own prompt modes

## Architecture Overview

```
Your Terminal
    ↓
CLI Interface (ollama-agent command)
    ↓
Cybersecurity Agent (chat management + prompts)
    ↓
Ollama Client (local model inference)
    ↓
Ollama Model (llama2, mistral, etc.)
```

Everything runs locally - your data never leaves your machine!

## Support Resources

- **Ollama Docs**: https://ollama.ai/docs
- **NIST Security**: https://www.nist.gov/cyberframework
- **OWASP**: https://owasp.org/
- **CIS Benchmarks**: https://www.cisecurity.org/

---

**Ready to get started?** Run: `bash quick_start.sh`

Or follow the steps above manually. Good luck! 🔒
