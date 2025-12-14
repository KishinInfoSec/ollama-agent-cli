"""Example test file for the Ollama Agent CLI"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_imports():
    """Test that all modules can be imported."""
    from ollama_agent import (
        OllamaSecurityAgent,
        get_prompt,
        list_available_modes,
        SECURITY_TOOLS,
    )
    
    assert OllamaSecurityAgent is not None
    assert callable(get_prompt)
    assert callable(list_available_modes)
    assert isinstance(SECURITY_TOOLS, list)


def test_prompts():
    """Test prompt functionality."""
    from ollama_agent import get_prompt, list_available_modes
    
    modes = list_available_modes()
    assert len(modes) > 0
    assert "default" in modes
    
    # Test getting a prompt
    prompt = get_prompt("default")
    assert isinstance(prompt, str)
    assert len(prompt) > 0


def test_tools():
    """Test tools module."""
    from ollama_agent.tools import get_tools_summary
    
    tools_info = get_tools_summary()
    assert isinstance(tools_info, str)
    assert "analyze_risk_level" in tools_info
    assert "get_cve_remediation" in tools_info
    assert "create_security_checklist" in tools_info
