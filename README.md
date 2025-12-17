# Ollama Cybersecurity Agent CLI

A powerful command-line tool for interacting with Ollama models as a cybersecurity agent with pre-built expert prompts and specialized tools.

## Features

- 🔒 **Cybersecurity-Focused**: 8 specialized prompt modes for different security domains
- 💬 **Interactive Chat**: Multi-turn conversations with context awareness
- 🛠️ **17 Built-in Tools**: File operations, search, git integration, risk analysis, CVE remediation, security checklists
- 🎨 **VS Code Tool Integration**: All VS Code-like tools (file search, grep, git operations, etc.)
- 🔄 **Streaming Responses**: Real-time response streaming from Ollama
- 📊 **Multiple Modes**: Threat analysis, incident response, vulnerability assessment, compliance, secure coding, network security, malware analysis
- 🎯 **Model Agnostic**: Works with any Ollama-supported model
- **✨ NEW: VS Code Tools** - 17 tools matching VS Code capabilities (find, grep, git, file ops)
- **✨ Structured Tool Calling** - JSON-based tool calling with Pydantic validation
- **✨ Full Observability** - OpenTelemetry tracing and metrics support
- **✨ Enhanced Error Handling** - Better validation and error messages

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running locally
- At least one model installed in Ollama (e.g., `ollama pull llama2`)

## Installation

### 1. Start Ollama Server

```bash
# Start Ollama service (if not already running)
ollama serve
```

### 2. Pull a Model

```bash
# Pull a model suitable for cybersecurity discussions
ollama pull llama2          # 7B parameter model
# or
ollama pull mistral         # Faster alternative
# or
ollama pull neural-chat     # Good for chat
```

### 3. Install the CLI Tool

```bash
cd /path/to/dir

# Option A: Development installation
pip install -e .

# Option B: Install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

### Check Connection

```bash
ollama-agent check-connection
```

### Interactive Mode

```bash
# Start interactive chat (default mode)
ollama-agent interactive

# With specific model and mode
ollama-agent interactive --model llama2 --mode threat_analysis --temperature 0.7
```

### Single Query

```bash
# Send a single query
ollama-agent query "Analyze the risks of SQL injection vulnerabilities in web applications"

# With specific settings
ollama-agent query "How to harden a Linux web server?" \
  --model llama2 \
  --mode network \
  --temperature 0.6
```

### List Available Modes

```bash
ollama-agent list-modes
```

## Available Prompt Modes

| Mode | Purpose |
|------|---------|
| `default` | General cybersecurity expertise |
| `threat_analysis` | Analyze threats, actors, and attack vectors |
| `incident_response` | Handle security incidents and forensics |
| `vulnerability` | Assess and remediate vulnerabilities |
| `compliance` | Security audits and compliance (NIST, CIS, ISO 27001) |
| `secure_coding` | Code review and secure development |
| `network` | Network security architecture and hardening |
| `malware` | Malware analysis and detection |

## Interactive Chat Commands

When in interactive mode, use these special commands:

```
/help      - Show help and available commands
/clear     - Clear conversation history
/mode <name> - Switch to different analysis mode
/modes     - List all available prompt modes
/models    - List available Ollama models
/tools     - Show available security tools
/exit      - Exit the agent
```

## Usage Examples

### Example 1: Threat Analysis

```bash
$ ollama-agent interactive --mode threat_analysis
```

```
You: What's the threat profile of ransomware targeting healthcare organizations?

Agent: Ransomware targeting healthcare organizations presents a critical threat...
```

### Example 2: Vulnerability Assessment

```bash
$ ollama-agent query "List the top OWASP vulnerabilities and how to prevent them" \
  --mode vulnerability
```

### Example 3: Incident Response

```bash
$ ollama-agent interactive --mode incident_response
```

```
You: We detected suspicious activity on our database server. What should we do?

Agent: This requires immediate action. Follow these incident response steps...
```

### Example 4: Compliance Audit

```bash
$ ollama-agent query "What are the key requirements for SOC 2 Type II compliance?" \
  --mode compliance
```

### Example 5: Secure Coding Review

```bash
$ ollama-agent query "Review this code for security vulnerabilities: [paste code]" \
  --mode secure_coding
```

## Built-in Tools

The agent has access to 17 specialized tools inspired by VS Code's extensible tool system.

### File Operations & Discovery (8 tools)
- `execute_command` - Run shell commands with timeout and working directory support
- `get_file_contents` - Read files with line range support
- `write_file` - Create/modify files with append mode
- `list_directory` - List directories with recursive option
- `create_directory` - Create directories recursively
- `delete_file` / `delete_directory` - Remove files and directories
- `copy_file` - Copy files with directory creation
- `find_files` - Find files by glob pattern (like VS Code's file search)
- `grep_search` - Search text with regex support (like VS Code's text search)
- `get_file_info` - Get file metadata (size, type, permissions)

### Git Operations (3 tools)
- `git_status` - Check repository status
- `git_log` - View recent commits
- `git_diff` - Show uncommitted changes

### Security Analysis (3 original tools)

1. **Risk Analysis** (`analyze_risk_level`)
   - Calculates risk scores based on threat severity
   - Assesses impact and affected systems
   - Provides severity ratings (CRITICAL, HIGH, MEDIUM, LOW)

2. **CVE Remediation** (`get_cve_remediation`)
   - Provides step-by-step remediation for known CVEs
   - Includes detection and prevention strategies
   - References official CVE data

3. **Security Checklists** (`create_security_checklist`)
   - Generates hardening checklists for:
     - Web applications
     - Network infrastructure
     - Cloud environments
   - Covers OWASP, CIS, and industry best practices

### Example Tool Usage in Chat

```
You: Search for all configuration files in the project

Agent: Let me find configuration files for you.

{"tool": "find_files", "parameters": {"pattern": "**/*.{json,yaml,yml,toml,conf}", "max_results": 20}}

[Tool 'find_files' executed]
Result: Found 5 file(s) matching...
```

For detailed documentation on all tools, see [VSCODE_TOOLS_INTEGRATION.md](VSCODE_TOOLS_INTEGRATION.md)

## Configuration

### Environment Variables

```bash
# Override default Ollama host
export OLLAMA_HOST="http://localhost:11434"
```

### Command-line Options

```bash
ollama-agent interactive \
  --model llama2              # Ollama model name
  --host http://localhost:11434  # Ollama server host
  --mode default             # Prompt mode
  --temperature 0.7          # Model temperature (0-1)
```

**Temperature Guide:**
- `0.0-0.3`: More focused and deterministic (better for technical questions)
- `0.4-0.7`: Balanced (recommended)
- `0.8-1.0`: More creative and varied responses

## Project Structure

```
ollama-agent-cli/
├── pyproject.toml              # Project configuration
├── README.md                   # This file
├── src/ollama_agent/
│   ├── __init__.py            # Package initialization
│   ├── agent.py               # Main agent implementation
│   ├── cli.py                 # CLI commands and interface
│   ├── prompts.py             # Cybersecurity prompt templates
│   └── tools.py               # Security analysis tools
└── examples/
    └── example_queries.txt    # Example security questions
```

## Performance Tips

1. **Model Selection**
   - Use smaller models (7B) for faster responses: `mistral`, `neural-chat`
   - Use larger models (13B+) for more detailed analysis: `llama2-13b`, `mixtral`

2. **Temperature Settings**
   - Technical questions: 0.3-0.5 (more deterministic)
   - Analysis/brainstorming: 0.6-0.8 (more creative)

3. **GPU Acceleration**
   - Ensure Ollama is using GPU if available for faster inference
   - Check with: `ollama ps`

## Troubleshooting

### Connection Error

```bash
# Error: Cannot connect to Ollama at http://localhost:11434

# Solution: Ensure Ollama is running
ollama serve

# Or check if running on different port
ollama-agent check-connection --host http://localhost:11435
```

### Model Not Found

```bash
# List available models
ollama-agent list-modes  # Lists prompt modes
ollama pull llama2       # Install a model

# Or specify available model
ollama-agent interactive --model mistral
```

### Slow Responses

```bash
# Use smaller, faster model
ollama-agent interactive --model neural-chat

# Or reduce temperature
ollama-agent interactive --temperature 0.5
```

## Advanced Usage

### Custom Workflows

Create a script to run multiple security analyses:

```bash
#!/bin/bash

echo "=== Security Audit Report ==="
echo ""

echo "1. Network Security Assessment"
ollama-agent query "Assess network security for a typical enterprise" --mode network

echo ""
echo "2. Vulnerability Review"
ollama-agent query "What are the most critical vulnerabilities to address?" --mode vulnerability

echo ""
echo "3. Compliance Check"
ollama-agent query "What compliance standards should we prioritize?" --mode compliance
```

### Piping Content

```bash
# Analyze a file for security issues
cat vulnerable_code.py | \
  ollama-agent query "Review this code for security vulnerabilities" --mode secure_coding
```

## Development

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Code Style

```bash
black src/
ruff check src/
```

## API Usage (Python)

You can also use the agent programmatically:

```python
from ollama_agent.agent import OllamaSecurityAgent

# Create agent
agent = OllamaSecurityAgent(model="llama2", prompt_mode="threat_analysis")

# Get response
response = agent.get_response("What is a zero-day vulnerability?")
print(response)

# Stream response
for chunk in agent.stream_response("Analyze this threat..."):
    print(chunk, end="", flush=True)

# Switch modes
agent.set_prompt_mode("incident_response")

# Get tools info
print(agent.get_tools_info())
```

## Contributing

Contributions welcome! Areas for enhancement:

- [ ] Additional security tools and integrations
- [ ] Support for remote Ollama instances with authentication
- [ ] Conversation export (JSON, markdown)
- [ ] Integration with threat intelligence feeds
- [ ] Custom prompt templates
- [ ] Batch query processing

## License

MIT License - Feel free to use and modify

## Support

For issues or questions:

1. Check that Ollama is running: `ollama serve`
2. Verify model is installed: `ollama list`
3. Test connection: `ollama-agent check-connection`
4. Review the examples in this README

## Resources

- [Ollama Documentation](https://ollama.ai/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)

---

**Happy analyzing! Stay secure! 🔒**
