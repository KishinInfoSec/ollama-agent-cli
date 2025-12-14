"""Ollama-based cybersecurity agent implementation"""

import ollama
import json
import re
from typing import Generator, Optional
from .prompts import get_prompt, list_available_modes
from .tools import (
    SECURITY_TOOLS, 
    get_tools_summary, 
    TOOL_SCHEMAS,
    get_tools_schema_for_prompt,
    get_tool_call_instructions,
    validate_tool_call,
)


class OllamaSecurityAgent:
    """Cybersecurity agent powered by Ollama"""
    
    def __init__(
        self,
        model: str = "llama2",
        host: str = "http://localhost:11434",
        prompt_mode: str = "default",
    ):
        """Initialize the Ollama security agent.
        
        Args:
            model: Ollama model name to use
            host: Ollama server host
            prompt_mode: System prompt mode (default, threat_analysis, incident_response, etc.)
        """
        self.model = model
        self.host = host
        self.prompt_mode = prompt_mode
        self.system_prompt = get_prompt(prompt_mode)
        self.client = ollama.Client(host=host)
        self.conversation_history = []
        
    def get_available_models(self) -> list[str]:
        """Get list of available models from Ollama server."""
        try:
            response = self.client.list()
            return [m["name"] for m in response["models"]]
        except Exception as e:
            return [f"Error: {str(e)}"]
    
    def get_available_prompt_modes(self) -> list[str]:
        """Get list of available prompt modes."""
        return list_available_modes()
    
    def get_tools_info(self) -> str:
        """Get information about available tools."""
        return get_tools_summary()
    
    def stream_response(
        self,
        message: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_tool_iterations: int = 3,
    ) -> Generator[str, None, None]:
        """Stream a response from the agent.
        
        Args:
            message: User message
            temperature: Model temperature parameter
            top_p: Model top_p parameter
            max_tool_iterations: Maximum number of tool execution iterations
            
        Yields:
            Response chunks as they stream from Ollama
        """
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        # Keep trying until we get a response without tool calls or max iterations reached
        iteration = 0
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Build the full prompt with conversation history
            prompt = self._build_prompt()
            
            try:
                # Stream response from Ollama
                response = self.client.generate(
                    model=self.model,
                    prompt=prompt,
                    stream=True,
                    options={
                        "temperature": temperature,
                        "top_p": top_p,
                    }
                )
                
                # Collect full response for processing
                full_response = ""
                for chunk in response:
                    if chunk.get("response"):
                        text = chunk["response"]
                        full_response += text
                        yield text
                
                # Check if the response contains tool calls
                processed_response, tools_executed = self._parse_and_execute_tools(full_response)
                
                if not tools_executed:
                    # No tool calls, we're done
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": full_response
                    })
                    break
                else:
                    # Tool calls were executed, add the processed response to history
                    # and continue to get another response from the model with the tool results
                    yield f"\n\n[Executing tools...]\n"
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": processed_response
                    })
                    # Loop will continue and generate a new response with tool results in context
                
            except Exception as e:
                yield f"\nError: {str(e)}"
                break
    
    def get_response(
        self,
        message: str,
        temperature: float = 0.7,
    ) -> str:
        """Get a complete response from the agent.
        
        Args:
            message: User message
            temperature: Model temperature parameter
            
        Returns:
            Complete response text
        """
        response = ""
        for chunk in self.stream_response(message, temperature=temperature):
            response += chunk
        return response
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []
    
    def set_prompt_mode(self, mode: str) -> bool:
        """Change the system prompt mode.
        
        Args:
            mode: Prompt mode name
            
        Returns:
            True if successful, False if mode not found
        """
        if mode not in list_available_modes():
            return False
        self.prompt_mode = mode
        self.system_prompt = get_prompt(mode)
        return True
    
    def _build_prompt(self) -> str:
        """Build the complete prompt with system instructions and history."""
        # Build tool descriptions
        tools_desc = get_tools_schema_for_prompt()
        tool_instructions = get_tool_call_instructions()
        
        prompt = f"""System: {self.system_prompt}

Available Tools:
{tools_desc}

{tool_instructions}

Conversation History:
"""
        
        # Add conversation history
        for msg in self.conversation_history:
            if msg["role"] == "user":
                prompt += f"\nUser: {msg['content']}"
            elif msg["role"] == "assistant":
                prompt += f"\nAssistant: {msg['content']}"
            elif msg["role"] == "tool":
                # Tool messages contain results
                func = msg.get("function", "unknown")
                result = msg.get("result", "")
                prompt += f"\n[Tool Result from '{func}']: {result}"
        
        # Add prompt for next response
        prompt += "\n\nAssistant: "
        return prompt
    
    def _get_tools_description(self) -> str:
        """Get descriptions of available tools."""
        descriptions = []
        for tool in SECURITY_TOOLS:
            name = tool.__name__
            doc = tool.__doc__ or "No description"
            descriptions.append(f"- {name}: {doc.split(chr(10))[0]}")
        return "\n".join(descriptions)
    
    def _execute_tool(self, function_name: str, parameters: dict) -> str:
        """Execute a tool and return the result."""
        # Validate the tool call
        is_valid, error_msg = validate_tool_call(function_name, parameters)
        if not is_valid:
            return f"Error: {error_msg}"
        
        # Find the tool
        tool_func = None
        for tool in SECURITY_TOOLS:
            if tool.__name__ == function_name:
                tool_func = tool
                break
        
        if not tool_func:
            return f"Error: Unknown tool '{function_name}'"
        
        try:
            # Call the tool with the provided parameters
            result = tool_func(**parameters)
            return result
        except TypeError as e:
            return f"Error: Invalid parameters for {function_name}: {str(e)}"
        except Exception as e:
            return f"Error executing {function_name}: {str(e)}"
    
    def _parse_and_execute_tools(self, response_text: str) -> tuple[str, bool]:
        """Parse response for tool calls and execute them.
        
        Looks for JSON tool calls in the format:
        {"tool": "tool_name", "parameters": {...}}
        
        Returns:
            Tuple of (processed_response, tools_were_executed)
        """
        # Look for JSON objects that look like tool calls
        json_pattern = r'\{["\']?tool["\']?\s*:\s*["\']([^"\']+)["\']\s*,\s*["\']?parameters["\']?\s*:\s*\{[^}]*\}\}'
        
        # Try to find tool calls in the response
        processed_response = response_text
        tools_executed = False
        
        # Split by potential JSON objects and process
        # Look for {"tool": "...", "parameters": {...}} patterns
        import re
        
        # Find all potential JSON tool calls
        lines = response_text.split('\n')
        for line in lines:
            # Try to parse as JSON
            line_stripped = line.strip()
            if line_stripped.startswith('{') and '"tool"' in line_stripped:
                try:
                    # Try to find the complete JSON object
                    brace_count = 0
                    json_str = ""
                    for char in line_stripped:
                        json_str += char
                        if char == '{':
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                        if brace_count == 0 and json_str:
                            break
                    
                    if json_str:
                        tool_call = json.loads(json_str)
                        
                        if "tool" in tool_call and "parameters" in tool_call:
                            function_name = tool_call["tool"]
                            parameters = tool_call.get("parameters", {})
                            
                            # Execute the tool
                            result = self._execute_tool(function_name, parameters)
                            
                            # Replace the tool call with the result
                            result_message = f"\n[Tool '{function_name}' executed]\nResult: {result}\n"
                            processed_response = processed_response.replace(json_str, result_message)
                            tools_executed = True
                            
                            # Add the tool call and result to history for context
                            self.conversation_history.append({
                                "role": "tool",
                                "function": function_name,
                                "result": result
                            })
                except (json.JSONDecodeError, ValueError):
                    # Not valid JSON, skip
                    pass
        
        return processed_response, tools_executed
    
    def test_connection(self) -> bool:
        """Test connection to Ollama server."""
        try:
            response = self.client.list()
            return True
        except Exception:
            return False
