# Ollama Cybersecurity Agent CLI - Documentation Guide

## 📚 Navigation by Task

**New to the project?** → [GETTING_STARTED.md](GETTING_STARTED.md)
**Want quick commands?** → [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
**Looking for examples?** → [EXAMPLES.md](EXAMPLES.md)
**Full reference guide?** → [README.md](README.md)
**Technical architecture?** → [ARCHITECTURE.md](ARCHITECTURE.md)
**Want to contribute?** → [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🚀 Quick Start (2 minutes)

```bash
# 1. Start Ollama server (in terminal 1)
ollama serve

# 2. Install (in terminal 2)
cd /path/to/dir
bash quick_start.sh

# 3. Run (in terminal 3)
ollama-agent interactive
```

---

## 📖 Documentation Files

| File | Purpose | Best For |
|------|---------|----------|
| **README.md** | Complete reference with all features and commands | General reference, troubleshooting |
| **GETTING_STARTED.md** | Step-by-step setup and first run | New users, first-time setup |
| **QUICK_REFERENCE.md** | Command cheat sheet and mode listing | Quick lookups, common tasks |
| **EXAMPLES.md** | Real-world cybersecurity queries | Learning by example |
| **ARCHITECTURE.md** | Technical design and extension points | Developers, customization |
| **CONTRIBUTING.md** | Development setup and contribution guide | Contributing code, adding features |

---

## 🎯 Common Scenarios

### "I want to get started quickly"
1. Read: [GETTING_STARTED.md](GETTING_STARTED.md) (5 min)
2. Run: `bash quick_start.sh`
3. Try: `ollama-agent interactive`

### "Show me what this can do"
- See: [README.md](README.md) - Features section
- Try: [EXAMPLES.md](EXAMPLES.md) - Real queries

### "I need quick commands"
- Reference: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- Help: `ollama-agent --help`

### "I want to customize it"
1. Learn: [ARCHITECTURE.md](ARCHITECTURE.md)
2. Guide: [CONTRIBUTING.md](CONTRIBUTING.md)
3. Edit: `src/ollama_agent/prompts.py` or `tools.py`

### "I'm having issues"
1. Check: [GETTING_STARTED.md](GETTING_STARTED.md#troubleshooting) - Troubleshooting section
2. Verify: `ollama-agent check-connection`
3. Read: [README.md](README.md#common-issues) - Common issues

### "I want to understand the code"
1. Start: [ARCHITECTURE.md](ARCHITECTURE.md)
2. Review: `src/ollama_agent/`
3. Contribute: [CONTRIBUTING.md](CONTRIBUTING.md)
- Troubleshooting

### 2. README.md
**Best for:** Complete reference
- Feature list
- Installation (detailed)
- Quick start
- All CLI commands
- 8 prompt modes explained
- Built-in tools
- Configuration
- Performance optimization
- Troubleshooting (detailed)
- Advanced usage
- Python API examples

### 3. EXAMPLES.md
**Best for:** Real-world scenarios
- Threat analysis examples
- Incident response examples
- Vulnerability assessment examples
- Compliance examples
- Secure coding examples
- Network security examples
- Malware analysis examples
- Interactive session example
- Batch processing script

### 4. PROJECT_SUMMARY.md
**Best for:** Project overview
- What's included
- Key features summary
- Quick start snippet
- Common use cases
- Troubleshooting quick links

### 5. ARCHITECTURE.md
**Best for:** Technical understanding
- System design
- Component breakdown
- Data flow
- Extension points
- Integration patterns
- Performance considerations
- Future roadmap

### 6. CONTRIBUTING.md
**Best for:** Development
- Setup for developers
- Code style
- Adding prompts
- Adding tools
- Testing
- PR checklist

---

## 🔑 Key Concepts

### Prompt Modes
The agent has 8 specialized modes for different security domains:

| Mode | Use Case |
|------|----------|
| `default` | General security questions |
| `threat_analysis` | Threat modeling and analysis |
| `incident_response` | Security incidents and forensics |
| `vulnerability` | CVE and vulnerability assessment |
| `compliance` | Audits and standards (NIST, CIS, ISO) |
| `secure_coding` | Code review and development |
| `network` | Network architecture and design |
| `malware` | Malware behavior and detection |

**How to use:**
```bash
ollama-agent interactive --mode threat_analysis
```

### Interactive Commands
Special commands available in interactive mode:

| Command | Purpose |
|---------|---------|
| `/help` | Show help |
| `/modes` | List available modes |
| `/models` | List installed models |
| `/tools` | Show available tools |
| `/clear` | Clear conversation |
| `/mode <name>` | Switch mode |
| `/exit` | Exit |

### Built-in Tools
- **Risk Analysis**: Score and assess threats
- **CVE Remediation**: Get fix guidance for known CVEs
- **Security Checklists**: Hardening checklists for different domains

---

## 🚀 Common Workflows

### Workflow 1: Initial Setup
1. Read: [GETTING_STARTED.md](GETTING_STARTED.md)
2. Run: `bash quick_start.sh`
3. Test: `ollama-agent check-connection`
4. Try: `ollama-agent query "Hello"`

### Workflow 2: First Security Analysis
1. Start: `ollama-agent interactive`
2. Ask: A cybersecurity question
3. Use: `/mode vulnerability` to switch modes
4. Explore: Different modes with `/modes`
5. Exit: `/exit`

### Workflow 3: Quick Query
1. Run: `ollama-agent query "Your security question"`
2. Or: `ollama-agent query "..." --mode threat_analysis`
3. Adjust: `--temperature 0.5` for different responses

### Workflow 4: Extended Analysis
1. Start: `ollama-agent interactive --mode incident_response`
2. Ask: Initial question
3. Follow-up: Ask follow-up questions (maintains context)
4. Switch: `/mode compliance` to change focus
5. Clear: `/clear` to reset conversation

### Workflow 5: Batch Processing
1. Create: Script with multiple queries
2. Run: See [EXAMPLES.md](EXAMPLES.md) for sample script
3. Save: Pipe output to file for report

---

## 📋 Feature Matrix

| Feature | Where to Learn |
|---------|---|
| Interactive chat | [README.md](README.md) + [EXAMPLES.md](EXAMPLES.md) |
| Single queries | [README.md](README.md) Usage section |
| Prompt modes (8 types) | [README.md](README.md) Modes section |
| Built-in tools | [README.md](README.md) + [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |
| Multi-turn context | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Custom prompts | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Custom tools | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Performance tuning | [README.md](README.md) Performance Tips |
| Troubleshooting | [GETTING_STARTED.md](GETTING_STARTED.md) + [README.md](README.md) |
| Python API | [README.md](README.md) API Usage |

---

## 🔧 Development Quick Links

- **Add Prompt Mode**: [CONTRIBUTING.md](CONTRIBUTING.md#adding-new-prompt-modes)
- **Add Tool**: [CONTRIBUTING.md](CONTRIBUTING.md#adding-new-tools)
- **Understand Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Code Style**: [CONTRIBUTING.md](CONTRIBUTING.md#code-style)
- **Testing**: [CONTRIBUTING.md](CONTRIBUTING.md#testing)

---

## 📞 Getting Help

### Problem: Can't connect to Ollama
→ [GETTING_STARTED.md](GETTING_STARTED.md) - Troubleshooting section

### Problem: Model not found
→ [README.md](README.md) - Troubleshooting section

### Problem: Slow responses
→ [README.md](README.md) - Performance Tips section

### Problem: Want to customize it
→ [CONTRIBUTING.md](CONTRIBUTING.md)

### Problem: Need real examples
→ [EXAMPLES.md](EXAMPLES.md)

### Problem: Want to understand the system
→ [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 📁 Project Files

### Documentation
```
README.md               - Main reference guide
GETTING_STARTED.md     - Beginner setup guide
EXAMPLES.md            - Real usage examples
PROJECT_SUMMARY.md     - Project overview
ARCHITECTURE.md        - Technical design
CONTRIBUTING.md        - Development guide
INDEX.md               - This file
```

### Core Code
```
src/ollama_agent/
├── __init__.py         - Package init
├── agent.py            - Main agent logic
├── cli.py              - Command-line interface
├── prompts.py          - 8 security prompt modes
└── tools.py            - Security analysis tools
```

### Configuration
```
pyproject.toml         - Project metadata & dependencies
setup.py               - Alternative setup configuration
.gitignore             - Git ignore patterns
```

### Utilities
```
quick_start.sh         - Automated setup script
```

---

## 🎓 Learning Path

### Beginner Path (30 minutes)
1. Read: [GETTING_STARTED.md](GETTING_STARTED.md) - 10 min
2. Install: `bash quick_start.sh` - 10 min
3. Try: `ollama-agent interactive` - 10 min

### Intermediate Path (1-2 hours)
1. Read: [README.md](README.md) - 30 min
2. Try: Examples from [EXAMPLES.md](EXAMPLES.md) - 30 min
3. Explore: Different modes and settings - 30 min

### Advanced Path (2-4 hours)
1. Read: [ARCHITECTURE.md](ARCHITECTURE.md) - 1 hour
2. Read: [CONTRIBUTING.md](CONTRIBUTING.md) - 30 min
3. Add: Custom prompt or tool - 1-2 hours

---

## ✅ Checklist: Getting Started

- [ ] Read [GETTING_STARTED.md](GETTING_STARTED.md)
- [ ] Install Ollama from https://ollama.ai
- [ ] Run `bash quick_start.sh`
- [ ] Test: `ollama-agent check-connection`
- [ ] Try: `ollama-agent interactive`
- [ ] Read: [README.md](README.md) for full reference
- [ ] Explore: Examples in [EXAMPLES.md](EXAMPLES.md)
- [ ] Customize: Follow [CONTRIBUTING.md](CONTRIBUTING.md) if needed

---

## 🎉 Ready to Start?

**Quickest way to get started:**
```bash
# 1. Install
bash quick_start.sh

# 2. Test
ollama-agent check-connection

# 3. Start using it
ollama-agent interactive
```

**Or read the full guide:**
[GETTING_STARTED.md](GETTING_STARTED.md)

---

**Happy analyzing! 🔒**

*Last updated: 2024*
*Version: 0.1.0*
