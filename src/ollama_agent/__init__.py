"""Ollama Agent CLI - Cybersecurity Agent Tool"""

from .agent import OllamaSecurityAgent
from .cli import app, main
from .tools import SECURITY_TOOLS, TOOL_SCHEMAS, validate_tool_call
from .prompts import get_prompt, list_available_modes
from .tracing import setup_tracing, TracedAgent

__version__ = "0.2.0"

__all__ = [
    "OllamaSecurityAgent",
    "app",
    "main",
    "SECURITY_TOOLS",
    "TOOL_SCHEMAS",
    "validate_tool_call",
    "get_prompt",
    "list_available_modes",
    "setup_tracing",
    "TracedAgent",
]
