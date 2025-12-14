# Ollama Cybersecurity Agent CLI - Architecture

## Overview

The Ollama Cybersecurity Agent CLI is designed as a modular, extensible system for security analysis and consultation powered by local Ollama models.

## Architecture

```
┌─────────────────────────────────────────────────┐
│           CLI Interface (cli.py)                 │
│  - Interactive chat mode                         │
│  - Single query mode                             │
│  - Mode/model switching                          │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│        Security Agent (agent.py)                 │
│  - Conversation management                       │
│  - Prompt building                               │
│  - Response streaming                            │
│  - Tool integration                              │
└──────────────┬──────────────────────────────────┘
               │
      ┌────────┴────────┬─────────────┐
      │                 │             │
      ▼                 ▼             ▼
┌──────────────┐ ┌───────────┐ ┌────────────┐
│ Prompts      │ │ Tools     │ │ Ollama     │
│ (prompts.py) │ │(tools.py) │ │ Client     │
├──────────────┤ ├───────────┤ └────────────┘
│- default     │ │- analyze_ │
│- threat_     │ │  risk_    │
│  analysis    │ │  level    │
│- incident    │ │- get_cve_ │
│  response    │ │  remediat │
│- vulner      │ │  ion      │
│  ability     │ │- create_  │
│- compliance  │ │  security │
│- secure_     │ │  _check   │
│  coding      │ │  list     │
│- network     │ │           │
│- malware     │ │           │
└──────────────┘ └───────────┘
```

## Component Breakdown

### 1. CLI Module (`cli.py`)
- **Responsibility**: Handle user interaction and command routing
- **Commands**:
  - `interactive`: Multi-turn conversation
  - `query`: Single query execution
  - `list-modes`: Show available prompt modes
  - `check-connection`: Verify Ollama connectivity
- **Features**:
  - Rich console output with colors and formatting
  - Real-time response streaming
  - Special command handling (/help, /clear, /exit, etc.)

### 2. Agent Module (`agent.py`)
- **Responsibility**: Core agent logic and Ollama interaction
- **Key Methods**:
  - `stream_response()`: Stream responses from Ollama
  - `get_response()`: Get complete response
  - `set_prompt_mode()`: Switch security analysis mode
  - `_build_prompt()`: Construct prompts with history
  - `test_connection()`: Verify Ollama server availability
- **Features**:
  - Multi-turn conversation with context
  - Configurable temperature and sampling
  - Model agnostic (works with any Ollama model)

### 3. Prompts Module (`prompts.py`)
- **Responsibility**: Cybersecurity-specific system prompts
- **Modes**:
  - 8 specialized prompt templates
  - Each tailored for different security domains
  - Extensible design for custom prompts
- **Benefits**:
  - Guides model behavior
  - Ensures relevant security expertise
  - Consistent response quality

### 4. Tools Module (`tools.py`)
- **Responsibility**: Security analysis utilities
- **Available Tools**:
  - Risk analysis and scoring
  - CVE remediation guidance
  - Security hardening checklists
- **Design**:
  - Type-annotated functions
  - Self-documenting with docstrings
  - Easily extensible

## Data Flow

### Interactive Mode Flow

```
User Input
    ↓
CLI.interactive()
    ↓
Special Command? → Handle & Continue
    ↓ No
OllamaSecurityAgent.stream_response()
    ↓
Build prompt with history
    ↓
Send to Ollama via ollama.Client
    ↓
Stream & Display Response
    ↓
Save to conversation history
    ↓
Ready for next input
```

### Single Query Flow

```
Command Line Args
    ↓
CLI.query()
    ↓
OllamaSecurityAgent.get_response()
    ↓
stream_response() internally
    ↓
Collect & Display Full Response
    ↓
Exit
```

## Extension Points

### Adding New Prompt Modes

1. Add to `prompts.py`:
```python
MY_NEW_MODE_PROMPT = """Your specialized system prompt here..."""
PROMPTS["my_mode"] = MY_NEW_MODE_PROMPT
```

2. Use via CLI:
```bash
ollama-agent interactive --mode my_mode
```

### Adding New Tools

1. Define in `tools.py`:
```python
def my_tool(
    param: Annotated[str, "Parameter description"]
) -> str:
    """Tool documentation."""
    # Implementation
    return result

SECURITY_TOOLS.append(my_tool)
```

2. Tools are automatically available to the agent

### Custom Temperature/Sampling

```python
agent.stream_response(message, temperature=0.5, top_p=0.8)
```

## Integration with Agent Framework

While this CLI uses native Ollama client for simplicity, it's designed to be compatible with Microsoft Agent Framework:

**Future Enhancement**:
```python
from agent_framework import ChatAgent
from agent_framework.ollama import OllamaClient

async def with_agent_framework():
    async with ChatAgent(
        chat_client=OllamaClient(...),
        instructions=get_prompt("default"),
        tools=SECURITY_TOOLS,
    ) as agent:
        result = await agent.run_stream(user_input)
```

## Performance Considerations

1. **Model Selection**:
   - Smaller (7B): Faster, lower resource usage
   - Larger (13B+): Better quality, more resource intensive

2. **Streaming**:
   - Provides real-time feedback
   - Better UX than waiting for complete response
   - Essential for interactive mode

3. **Conversation History**:
   - Limited to runtime memory
   - Provide context for coherent multi-turn conversations
   - Can be cleared to free memory

## Security Considerations

1. **Local Execution**: All processing happens locally, no cloud transmission
2. **Model Trust**: Use trusted Ollama models
3. **Input Validation**: Sanitize user prompts if needed
4. **No Sensitive Data Storage**: Conversation history only in memory

## Testing Strategy

```
Unit Tests:
  - Prompt loading and switching
  - Tool execution and output
  - Connection validation

Integration Tests:
  - Full CLI command flows
  - Agent-Ollama interaction
  - Multi-turn conversations

Manual Testing:
  - Various security scenarios
  - Different prompt modes
  - Model switching
```

## Future Enhancements

1. **Persistent Storage**: Save conversations to database
2. **Multi-Agent Orchestration**: Coordinate multiple specialized agents
3. **External Tool Integration**: APIs for threat intel, vulnerability databases
4. **Web UI**: Interactive web interface alongside CLI
5. **Batch Processing**: Process multiple security queries from files
6. **Custom Model Fine-tuning**: Specialized models for specific domains
7. **Evaluation Framework**: Assess response quality and accuracy
8. **Tracing & Observability**: Debug and monitor agent behavior
