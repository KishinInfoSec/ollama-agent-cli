# Contributing to Ollama Cybersecurity Agent CLI

Thank you for your interest in contributing!

## Development Setup

```bash
# Clone and setup
cd /home/alex/opencti/ollama-agent-cli

# Install in development mode with test dependencies
pip install -e ".[dev]"
```

## Code Style

We use Black and Ruff for code formatting:

```bash
# Format code
black src/

# Check for linting issues
ruff check src/
```

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src/ollama_agent
```

## Adding New Prompt Modes

1. Define the prompt in `src/ollama_agent/prompts.py`:

```python
MY_DOMAIN_PROMPT = """You are an expert in [domain]...
When analyzing [domain] issues:
1. First step
2. Second step
...
"""
```

2. Add to the PROMPTS dictionary:

```python
PROMPTS["my_domain"] = MY_DOMAIN_PROMPT
```

3. Test it:

```bash
ollama-agent query "Your question" --mode my_domain
```

## Adding New Tools

1. Define in `src/ollama_agent/tools.py`:

```python
def my_security_tool(
    param1: Annotated[str, "Description"],
    param2: Annotated[int, "Description"],
) -> str:
    """Tool description.
    
    Args:
        param1: What it does
        param2: What it does
        
    Returns:
        Analysis result
    """
    # Implementation
    return result
```

2. Add to SECURITY_TOOLS list:

```python
SECURITY_TOOLS.append(my_security_tool)
```

3. Update `get_tools_summary()` with the new tool

## PR Checklist

- [ ] Code formatted with Black
- [ ] Passes Ruff linting
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Follows existing code patterns
- [ ] No hardcoded values (use constants)

## Areas for Contribution

- [ ] Additional security prompts/modes
- [ ] More specialized tools
- [ ] Better error handling
- [ ] Performance improvements
- [ ] Documentation improvements
- [ ] Test coverage expansion
- [ ] Integration with threat feeds
- [ ] Multi-language support

## Questions?

Open an issue on GitHub or contact the maintainers.
