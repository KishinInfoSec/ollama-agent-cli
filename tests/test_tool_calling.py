"""Comprehensive tests for the Ollama Agent CLI with tool calling"""

import sys
from pathlib import Path
import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_imports():
    """Test that all modules can be imported."""
    from ollama_agent import (
        OllamaSecurityAgent,
        get_prompt,
        list_available_modes,
        SECURITY_TOOLS,
        TOOL_SCHEMAS,
        validate_tool_call,
        setup_tracing,
        TracedAgent,
    )
    
    assert OllamaSecurityAgent is not None
    assert callable(get_prompt)
    assert callable(list_available_modes)
    assert isinstance(SECURITY_TOOLS, list)
    assert isinstance(TOOL_SCHEMAS, dict)
    assert callable(validate_tool_call)
    assert callable(setup_tracing)


def test_prompts():
    """Test prompt functionality."""
    from ollama_agent import get_prompt, list_available_modes
    
    modes = list_available_modes()
    assert len(modes) > 0
    assert "default" in modes
    assert "threat_analysis" in modes
    
    # Test getting a prompt
    prompt = get_prompt("default")
    assert isinstance(prompt, str)
    assert len(prompt) > 0


def test_tools_basic():
    """Test tools module."""
    from ollama_agent.tools import get_tools_summary, get_tools_schema_for_prompt, get_tool_call_instructions
    
    tools_info = get_tools_summary()
    assert isinstance(tools_info, str)
    assert "analyze_risk_level" in tools_info
    assert "get_cve_remediation" in tools_info
    assert "create_security_checklist" in tools_info
    
    # Test schema output
    schemas = get_tools_schema_for_prompt()
    assert "execute_command" in schemas
    
    # Test instructions
    instructions = get_tool_call_instructions()
    assert "tool" in instructions


def test_tool_schemas():
    """Test tool schema definitions."""
    from ollama_agent.tools import TOOL_SCHEMAS
    
    expected_tools = [
        "execute_command",
        "get_file_contents",
        "write_file",
        "list_directory",
        "analyze_risk_level",
        "get_cve_remediation",
        "create_security_checklist",
    ]
    
    for tool in expected_tools:
        assert tool in TOOL_SCHEMAS
        schema = TOOL_SCHEMAS[tool]
        assert schema.name == tool
        assert schema.description
        assert schema.parameters


def test_tool_validation():
    """Test tool parameter validation."""
    from ollama_agent.tools import validate_tool_call
    
    # Valid execute_command
    is_valid, error = validate_tool_call("execute_command", {"command": "ls"})
    assert is_valid, error
    assert error == ""
    
    # Missing required parameter
    is_valid, error = validate_tool_call("execute_command", {})
    assert not is_valid
    assert "required parameter" in error.lower()
    
    # Unknown tool
    is_valid, error = validate_tool_call("unknown_tool", {})
    assert not is_valid
    assert "unknown" in error.lower()
    
    # Wrong type for analyze_risk_level
    is_valid, error = validate_tool_call(
        "analyze_risk_level",
        {
            "threat_name": "Test",
            "affected_systems": "not_a_number",  # Should be int
            "data_exposure": True
        }
    )
    assert not is_valid
    assert "integer" in error.lower() or "type" in error.lower()


def test_agent_initialization():
    """Test agent initialization."""
    from ollama_agent import OllamaSecurityAgent
    
    agent = OllamaSecurityAgent()
    assert agent.model == "llama2"
    assert agent.system_prompt
    assert agent.conversation_history == []
    assert agent.prompt_mode == "default"


def test_agent_methods():
    """Test agent methods."""
    from ollama_agent import OllamaSecurityAgent
    
    agent = OllamaSecurityAgent()
    
    # Test clear history
    agent.conversation_history.append({"role": "user", "content": "test"})
    agent.clear_history()
    assert len(agent.conversation_history) == 0
    
    # Test set prompt mode
    result = agent.set_prompt_mode("threat_analysis")
    assert result
    assert agent.prompt_mode == "threat_analysis"
    
    # Invalid mode
    result = agent.set_prompt_mode("nonexistent")
    assert not result
    
    # Test getting modes
    modes = agent.get_available_prompt_modes()
    assert "default" in modes
    
    # Test getting tools info
    info = agent.get_tools_info()
    assert "execute_command" in info


def test_tool_execution():
    """Test tool execution in agent."""
    from ollama_agent import OllamaSecurityAgent
    
    agent = OllamaSecurityAgent()
    
    # Test analyze_risk_level
    result = agent._execute_tool(
        "analyze_risk_level",
        {
            "threat_name": "Test Threat",
            "affected_systems": 100,
            "data_exposure": True
        }
    )
    assert "Risk Assessment" in result
    assert "CRITICAL" in result or "HIGH" in result or "MEDIUM" in result or "LOW" in result
    
    # Test with invalid tool
    result = agent._execute_tool("nonexistent", {})
    assert "Error" in result or "Unknown" in result


def test_tool_parsing():
    """Test tool call parsing."""
    from ollama_agent import OllamaSecurityAgent
    
    agent = OllamaSecurityAgent()
    
    # No tool calls
    response = "This is just a normal response"
    processed, executed = agent._parse_and_execute_tools(response)
    assert processed == response
    assert not executed
    
    # Response with tool call
    response_with_tool = '{"tool": "execute_command", "parameters": {"command": "echo test"}}'
    processed, executed = agent._parse_and_execute_tools(response_with_tool)
    # It should try to parse and execute
    assert executed or "[Tool" in processed


def test_tracing_setup():
    """Test tracing setup."""
    from ollama_agent.tracing import setup_tracing
    
    # Test with disabled tracing
    tracer, meter = setup_tracing(enabled=False)
    assert tracer is None
    assert meter is None


def test_traced_agent():
    """Test TracedAgent wrapper."""
    from ollama_agent import OllamaSecurityAgent, TracedAgent
    
    agent = OllamaSecurityAgent()
    traced_agent = TracedAgent(agent, tracer=None, meter=None)
    
    # Should delegate to wrapped agent
    assert traced_agent.model == agent.model
    assert traced_agent.system_prompt == agent.system_prompt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
