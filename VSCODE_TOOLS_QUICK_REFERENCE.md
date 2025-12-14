# VS Code Tools Quick Reference

Quick lookup guide for all 17 tools available in your Ollama agent.

## Terminal & Execution

### execute_command
Execute shell commands with timeout support.
```json
{"tool": "execute_command", "parameters": {"command": "ls -la", "timeout": 30, "cwd": "."}}
```

## File Operations

### get_file_contents
Read file contents with optional line ranges.
```json
{"tool": "get_file_contents", "parameters": {"filepath": "src/main.py", "start_line": 1, "end_line": 50}}
```

### write_file
Write or append content to files.
```json
{"tool": "write_file", "parameters": {"filepath": "output.txt", "content": "Hello", "append": false}}
```

### list_directory
List directory contents.
```json
{"tool": "list_directory", "parameters": {"dirpath": "src", "recursive": false}}
```

### create_directory
Create directories recursively.
```json
{"tool": "create_directory", "parameters": {"dirpath": "output/results"}}
```

### delete_file
Delete a file.
```json
{"tool": "delete_file", "parameters": {"filepath": "temp.txt"}}
```

### delete_directory
Delete a directory.
```json
{"tool": "delete_directory", "parameters": {"dirpath": "temp", "recursive": true}}
```

### copy_file
Copy a file.
```json
{"tool": "copy_file", "parameters": {"source": "file.txt", "destination": "backup/file.txt"}}
```

## Search & Discovery

### find_files
Find files by glob pattern.
```json
{"tool": "find_files", "parameters": {"pattern": "**/*.py", "dirpath": ".", "max_results": 50}}
```

**Common patterns:**
- `*.py` - All Python files
- `**/*.json` - All JSON files recursively
- `**/*.{py,js,ts}` - Multiple extensions
- `src/**/*.py` - Python files in src directory

### grep_search
Search for text in files.
```json
{"tool": "grep_search", "parameters": {"pattern": "TODO", "dirpath": ".", "file_pattern": "*.py", "is_regex": false, "case_sensitive": false}}
```

**Regex search example:**
```json
{"tool": "grep_search", "parameters": {"pattern": "def \\w+\\(", "dirpath": "src", "is_regex": true}}
```

### get_file_info
Get file metadata.
```json
{"tool": "get_file_info", "parameters": {"filepath": "package.json"}}
```

## Git Operations

### git_status
Check git status.
```json
{"tool": "git_status", "parameters": {"repo_path": "."}}
```

### git_log
View recent commits.
```json
{"tool": "git_log", "parameters": {"repo_path": ".", "max_commits": 10}}
```

### git_diff
Show uncommitted changes.
```json
{"tool": "git_diff", "parameters": {"repo_path": ".", "filepath": ""}}
```

## Security Analysis

### analyze_risk_level
Analyze security threat risk.
```json
{"tool": "analyze_risk_level", "parameters": {"threat_name": "SQL Injection", "affected_systems": 50, "data_exposure": true}}
```

### get_cve_remediation
Get CVE remediation guidance.
```json
{"tool": "get_cve_remediation", "parameters": {"cve_id": "CVE-2024-1234", "product": "Apache Log4j"}}
```

### create_security_checklist
Generate security checklist.
```json
{"tool": "create_security_checklist", "parameters": {"topic": "web_app"}}
```

**Available topics:** `web_app`, `network`, `cloud`

---

## Common Use Cases

### Search for security issues
```json
{"tool": "grep_search", "parameters": {"pattern": "TODO|FIXME|SECURITY|BUG|XXX", "dirpath": ".", "file_pattern": "*.py", "is_regex": true}}
```

### Find all configuration files
```json
{"tool": "find_files", "parameters": {"pattern": "**/*.{json,yaml,yml,toml,conf,env}"}}
```

### Get recent changes
```json
{"tool": "git_log", "parameters": {"repo_path": ".", "max_commits": 5}}
{"tool": "git_diff", "parameters": {"repo_path": "."}}
```

### List project structure
```json
{"tool": "list_directory", "parameters": {"dirpath": ".", "recursive": true}}
```

### Check file sizes
```json
{"tool": "find_files", "parameters": {"pattern": "**/*.py"}}
{"tool": "get_file_info", "parameters": {"filepath": "src/main.py"}}
```

---

## Tips

1. **Line Ranges**: Use `start_line` and `end_line` to read specific parts of large files
2. **Recursive Search**: Use `**` in glob patterns for recursive search (e.g., `**/*.py`)
3. **Regex Patterns**: Enable `is_regex` for complex pattern matching in `grep_search`
4. **Case Sensitivity**: Use `case_sensitive: false` for more flexible text search
5. **Result Limits**: All search tools have `max_results` to prevent overwhelming output
6. **Working Directory**: Use `cwd` in `execute_command` to run commands in specific directories
7. **Append Mode**: Use `append: true` in `write_file` to add to existing files

---

## Troubleshooting

**"Not a git repository" error**
- Make sure you're in a git repository directory
- Use `repo_path` parameter to specify the correct repository path

**File not found**
- Check that the path is correct and relative to the current working directory
- Use `find_files` to locate the file first

**Search returns no results**
- Try simplifying your regex pattern
- Increase `max_results` limit
- Try `case_sensitive: false`

**Command timeout**
- Increase the `timeout` parameter in `execute_command`
- Break large operations into smaller commands

---

See [VSCODE_TOOLS_INTEGRATION.md](VSCODE_TOOLS_INTEGRATION.md) for complete documentation.
