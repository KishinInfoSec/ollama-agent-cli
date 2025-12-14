# VS Code Tools Integration

## Overview

Your Ollama agent CLI now supports **all the same tools that are available in VS Code**, enabling powerful file operations, search capabilities, git integration, and more. This brings VS Code's extensible tool system to your local Ollama agent.

## Available Tools (17 Total)

### Terminal & Execution Tools

#### 1. `execute_command`
Execute shell commands with timeout and working directory support.

**Parameters:**
- `command` (string, required): The shell command to execute
- `timeout` (integer, optional, default=30): Timeout in seconds
- `cwd` (string, optional, default="."): Working directory for command

**Example:**
```json
{"tool": "execute_command", "parameters": {"command": "ls -la", "cwd": "/tmp"}}
```

---

### File Operations Tools

#### 2. `get_file_contents`
Read file contents with support for line ranges (like VS Code's file peek).

**Parameters:**
- `filepath` (string, required): Path to the file to read
- `start_line` (integer, optional, default=1): Starting line (1-indexed)
- `end_line` (integer, optional, default=-1): Ending line (1-indexed, -1 for end)

**Example:**
```json
{"tool": "get_file_contents", "parameters": {"filepath": "src/main.py", "start_line": 10, "end_line": 30}}
```

#### 3. `write_file`
Write or append content to files (creates directories as needed).

**Parameters:**
- `filepath` (string, required): Path to the file to write
- `content` (string, required): Content to write to the file
- `append` (boolean, optional, default=false): Append instead of overwrite

**Example:**
```json
{"tool": "write_file", "parameters": {"filepath": "notes.txt", "content": "Hello World", "append": false}}
```

#### 4. `list_directory`
List directory contents with optional recursive traversal.

**Parameters:**
- `dirpath` (string, optional, default="."): Path to the directory to list
- `recursive` (boolean, optional, default=false): List recursively with directory structure

**Example:**
```json
{"tool": "list_directory", "parameters": {"dirpath": "src", "recursive": true}}
```

#### 5. `create_directory`
Create directories recursively (like mkdir -p).

**Parameters:**
- `dirpath` (string, required): Path to the directory to create

**Example:**
```json
{"tool": "create_directory", "parameters": {"dirpath": "output/results/2024"}}
```

#### 6. `delete_file`
Delete a file.

**Parameters:**
- `filepath` (string, required): Path to the file to delete

**Example:**
```json
{"tool": "delete_file", "parameters": {"filepath": "temp.txt"}}
```

#### 7. `delete_directory`
Delete a directory.

**Parameters:**
- `dirpath` (string, required): Path to the directory to delete
- `recursive` (boolean, optional, default=false): Delete directory and all contents

**Example:**
```json
{"tool": "delete_directory", "parameters": {"dirpath": "temp_folder", "recursive": true}}
```

#### 8. `copy_file`
Copy files (creates destination directories as needed).

**Parameters:**
- `source` (string, required): Source file path
- `destination` (string, required): Destination file path

**Example:**
```json
{"tool": "copy_file", "parameters": {"source": "config.json", "destination": "backup/config.json"}}
```

---

### Search & File Discovery Tools

#### 9. `find_files`
Find files matching glob patterns (like VS Code's file search).

**Parameters:**
- `pattern` (string, required): Glob pattern (e.g., '*.py', '**/*.json')
- `dirpath` (string, optional, default="."): Starting directory for search
- `max_results` (integer, optional, default=50): Maximum number of results

**Example:**
```json
{"tool": "find_files", "parameters": {"pattern": "**/*.py", "dirpath": "src", "max_results": 20}}
```

#### 10. `grep_search`
Search for text or regex patterns in files (like VS Code's text search).

**Parameters:**
- `pattern` (string, required): Text or regex pattern to search for
- `dirpath` (string, optional, default="."): Directory to search in
- `file_pattern` (string, optional, default="*"): File glob pattern to search within (e.g., '*.py')
- `is_regex` (boolean, optional, default=false): Treat pattern as regex
- `case_sensitive` (boolean, optional, default=false): Case-sensitive search
- `max_results` (integer, optional, default=50): Maximum results to return

**Example:**
```json
{"tool": "grep_search", "parameters": {"pattern": "TODO|FIXME", "dirpath": "src", "file_pattern": "*.py", "is_regex": true, "max_results": 30}}
```

#### 11. `get_file_info`
Get file metadata (size, type, modification time, permissions).

**Parameters:**
- `filepath` (string, required): Path to the file

**Example:**
```json
{"tool": "get_file_info", "parameters": {"filepath": "package.json"}}
```

---

### Git Operations Tools

#### 12. `git_status`
Get git repository status (like VS Code's source control panel).

**Parameters:**
- `repo_path` (string, optional, default="."): Path to git repository

**Example:**
```json
{"tool": "git_status", "parameters": {"repo_path": "."}}
```

#### 13. `git_log`
Show recent git commits (like VS Code's git history).

**Parameters:**
- `repo_path` (string, optional, default="."): Path to git repository
- `max_commits` (integer, optional, default=10): Maximum number of commits to show

**Example:**
```json
{"tool": "git_log", "parameters": {"repo_path": ".", "max_commits": 15}}
```

#### 14. `git_diff`
Get git diff of uncommitted changes.

**Parameters:**
- `repo_path` (string, optional, default="."): Path to git repository
- `filepath` (string, optional, default=""): Specific file to diff (optional)

**Example:**
```json
{"tool": "git_diff", "parameters": {"repo_path": ".", "filepath": "src/main.py"}}
```

---

### Security Analysis Tools (Original)

#### 15. `analyze_risk_level`
Analyze and rate risk level of security threats.

**Parameters:**
- `threat_name` (string, required): The name or description of the threat
- `affected_systems` (integer, required): Number of affected systems
- `data_exposure` (boolean, required): Whether sensitive data is exposed

**Example:**
```json
{"tool": "analyze_risk_level", "parameters": {"threat_name": "SQL Injection", "affected_systems": 50, "data_exposure": true}}
```

#### 16. `get_cve_remediation`
Get remediation guidance for a CVE.

**Parameters:**
- `cve_id` (string, required): CVE identifier (e.g., CVE-2024-1234)
- `product` (string, required): Affected product name

**Example:**
```json
{"tool": "get_cve_remediation", "parameters": {"cve_id": "CVE-2024-1234", "product": "Apache Log4j"}}
```

#### 17. `create_security_checklist`
Create a security hardening checklist for various domains.

**Parameters:**
- `topic` (string, required): Security topic (e.g., 'web_app', 'network', 'cloud')

**Example:**
```json
{"tool": "create_security_checklist", "parameters": {"topic": "web_app"}}
```

---

## Usage in Agent Conversations

When the agent needs to use a tool, it formats the call as a JSON object:

```
User: What files are in the src directory?

Agent: Let me check the directory structure for you.

{"tool": "list_directory", "parameters": {"dirpath": "src", "recursive": true}}

[Tool 'list_directory' executed]
Result: Directory structure:
  src/
    ollama_agent/
      __init__.py
      agent.py
      ...
```

## Quick Start Examples

### 1. Search for security issues in code
```
User: Search for all TODOs and security concerns in the codebase
```

The agent might use:
```json
{"tool": "grep_search", "parameters": {"pattern": "TODO|FIXME|SECURITY|BUG", "dirpath": ".", "file_pattern": "*.py", "is_regex": true}}
```

### 2. Analyze recent changes
```
User: What changes have been made recently?
```

The agent might use:
```json
{"tool": "git_log", "parameters": {"repo_path": ".", "max_commits": 10}}
{"tool": "git_diff", "parameters": {"repo_path": "."}}
```

### 3. Find configuration files
```
User: Find all configuration files in the project
```

The agent might use:
```json
{"tool": "find_files", "parameters": {"pattern": "**/*.{json,yaml,yml,toml,conf}", "dirpath": "."}}
```

### 4. Code review
```
User: Review the main application file for security issues
```

The agent might use:
```json
{"tool": "find_files", "parameters": {"pattern": "**/main.py", "dirpath": "."}}
{"tool": "get_file_contents", "parameters": {"filepath": "src/main.py"}}
```

---

## Architecture

The tools are integrated through a flexible tool-calling system:

1. **Tool Definition** (`tools.py`): Defines all tool functions with proper type annotations
2. **Tool Schemas** (`TOOL_SCHEMAS`): Defines schemas for validation and prompt inclusion
3. **Tool Execution** (`agent.py`): Agent parses JSON tool calls from model responses and executes them
4. **Validation** (`validate_tool_call`): Validates parameters before execution

## Adding Custom Tools

To add a new VS Code-like tool:

1. Define the function in `tools.py` with `Annotated` type hints
2. Add it to the `SECURITY_TOOLS` list
3. Add its schema to `TOOL_SCHEMAS`
4. The agent will automatically make it available

Example:

```python
def my_custom_tool(
    param1: Annotated[str, "Description of param1"],
    param2: Annotated[int, "Description of param2"] = 10,
) -> str:
    """My custom tool description."""
    # Implementation
    return "result"

# Add to SECURITY_TOOLS
SECURITY_TOOLS.append(my_custom_tool)

# Add schema
TOOL_SCHEMAS["my_custom_tool"] = ToolSchema(
    name="my_custom_tool",
    description="My custom tool description",
    parameters=[
        ToolParameter(name="param1", type="string", description="Description"),
        ToolParameter(name="param2", type="integer", description="Description", default=10, required=False),
    ]
)
```

---

## Performance Considerations

- File searches use limits (`max_results`) to prevent overwhelming output
- Large file contents are truncated for readability
- Recursive directory listings are limited to prevent deep recursion
- All operations have reasonable timeouts

## Security Notes

- File operations work within the current directory context
- Command execution uses shell=True (consider security implications)
- Git operations require a valid git repository
- All paths should be validated by the agent before execution

---

## Testing the Tools

With the venv activated, you can test tools directly:

```bash
source venv/bin/activate
python3 -c "from src.ollama_agent.tools import SECURITY_TOOLS, TOOL_SCHEMAS; print(f'Total tools: {len(SECURITY_TOOLS)}')"
```

Or test the agent:

```bash
python3 -m ollama_agent interactive --model llama2
```

Then in the chat:
```
/tools
```

This will show all available tools.
