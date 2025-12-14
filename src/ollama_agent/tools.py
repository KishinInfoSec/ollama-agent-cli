"""Security-focused tools and utilities for the cybersecurity agent

This module provides a comprehensive set of tools compatible with VS Code's tool system,
including file operations, terminal commands, search capabilities, and git operations.
"""

from typing import Annotated, Callable, Any
import json
import subprocess
import os
import re
import glob
import glob as glob_module
import fnmatch
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field
from enum import Enum


# ============ TERMINAL & EXECUTION TOOLS ============

def execute_command(
    command: Annotated[str, "The shell command to execute"],
    timeout: Annotated[int, "Timeout in seconds (default 30)"] = 30,
    cwd: Annotated[str, "Working directory for command execution"] = ".",
) -> str:
    """Execute a shell command and return the output.
    
    Args:
        command: Shell command to execute
        timeout: Timeout in seconds
        cwd: Working directory
        
    Returns:
        Command output or error message
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd
        )
        output = result.stdout if result.stdout else result.stderr
        return f"Command executed successfully:\n{output}" if output else "Command executed (no output)"
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout} seconds"
    except Exception as e:
        return f"Error executing command: {str(e)}"


# ============ FILE OPERATIONS ============

def get_file_contents(
    filepath: Annotated[str, "Path to the file to read"],
    start_line: Annotated[int, "Starting line number (1-indexed, optional)"] = 1,
    end_line: Annotated[int, "Ending line number (1-indexed, optional)"] = -1,
) -> str:
    """Read and return the contents of a file.
    
    Args:
        filepath: Path to the file
        start_line: Starting line (1-indexed)
        end_line: Ending line (1-indexed, -1 for end of file)
        
    Returns:
        File contents or error message
    """
    try:
        if not os.path.exists(filepath):
            return f"Error: File not found: {filepath}"
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # Handle line range
        if end_line == -1:
            end_line = len(lines)
        
        # Adjust to 0-indexed
        start_idx = max(0, start_line - 1)
        end_idx = min(len(lines), end_line)
        
        selected_lines = lines[start_idx:end_idx]
        contents = "".join(selected_lines)
        
        # Limit output to first 5000 chars
        if len(contents) > 5000:
            return f"File contents (lines {start_line}-{end_line}, first 5000 chars):\n{contents[:5000]}\n\n[... truncated ...]"
        return f"File contents (lines {start_line}-{end_line}):\n{contents}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


def write_file(
    filepath: Annotated[str, "Path to the file to write"],
    content: Annotated[str, "Content to write to the file"],
    append: Annotated[bool, "Append to file instead of overwriting"] = False,
) -> str:
    """Write content to a file.
    
    Args:
        filepath: Path to the file
        content: Content to write
        append: Whether to append instead of overwrite
        
    Returns:
        Success or error message
    """
    try:
        # Create directories if needed
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)
        
        mode = 'a' if append else 'w'
        with open(filepath, mode, encoding='utf-8') as f:
            f.write(content)
        
        action = "appended to" if append else "wrote to"
        return f"Successfully {action} {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


def list_directory(
    dirpath: Annotated[str, "Path to the directory to list"] = ".",
    recursive: Annotated[bool, "List recursively with directory structure"] = False,
) -> str:
    """List files and directories in a path.
    
    Args:
        dirpath: Directory path (default: current directory)
        recursive: Whether to list recursively
        
    Returns:
        Directory listing or error message
    """
    try:
        if not os.path.exists(dirpath):
            return f"Error: Directory not found: {dirpath}"
        
        if recursive:
            # Tree-like recursive listing
            lines = []
            for root, dirs, files in os.walk(dirpath):
                level = root.replace(dirpath, '').count(os.sep)
                indent = ' ' * 2 * level
                lines.append(f"{indent}{os.path.basename(root)}/")
                sub_indent = ' ' * 2 * (level + 1)
                for file in sorted(files):
                    lines.append(f"{sub_indent}{file}")
            return "Directory structure:\n" + "\n".join(lines[:100])  # Limit output
        else:
            items = os.listdir(dirpath)
            listing = "\n".join([f"  {'[DIR]' if os.path.isdir(os.path.join(dirpath, item)) else '[FILE]'} {item}" for item in sorted(items)])
            return f"Contents of {dirpath}:\n{listing}"
    except Exception as e:
        return f"Error listing directory: {str(e)}"


# ============ SEARCH & FILE DISCOVERY ============

def find_files(
    pattern: Annotated[str, "Glob pattern to search for files (e.g., '**/*.py')"],
    dirpath: Annotated[str, "Starting directory for search"] = ".",
    max_results: Annotated[int, "Maximum number of results to return"] = 50,
) -> str:
    """Find files matching a glob pattern.
    
    Args:
        pattern: Glob pattern (e.g., '*.py', '**/*.json')
        dirpath: Starting directory
        max_results: Maximum results to return
        
    Returns:
        List of matching files or error message
    """
    try:
        if not os.path.exists(dirpath):
            return f"Error: Directory not found: {dirpath}"
        
        # Create full pattern path
        full_pattern = os.path.join(dirpath, pattern)
        matches = glob.glob(full_pattern, recursive=True)
        
        # Sort and limit results
        matches = sorted(matches)[:max_results]
        
        if not matches:
            return f"No files found matching pattern: {pattern}"
        
        result = f"Found {len(matches)} file(s) matching '{pattern}':\n"
        result += "\n".join(matches)
        return result
    except Exception as e:
        return f"Error finding files: {str(e)}"


def grep_search(
    pattern: Annotated[str, "Text pattern or regex to search for"],
    dirpath: Annotated[str, "Directory to search in"] = ".",
    file_pattern: Annotated[str, "File pattern to search within (e.g., '*.py')"] = "*",
    is_regex: Annotated[bool, "Treat pattern as regex"] = False,
    case_sensitive: Annotated[bool, "Case-sensitive search"] = False,
    max_results: Annotated[int, "Maximum number of results"] = 50,
) -> str:
    """Search for text in files (grep-like functionality).
    
    Args:
        pattern: Text or regex pattern to search for
        dirpath: Directory to search in
        file_pattern: File glob pattern to search within
        is_regex: Whether to treat pattern as regex
        case_sensitive: Whether search is case-sensitive
        max_results: Maximum results to return
        
    Returns:
        Search results with file paths and line numbers
    """
    try:
        if not os.path.exists(dirpath):
            return f"Error: Directory not found: {dirpath}"
        
        results = []
        flags = 0 if case_sensitive else re.IGNORECASE
        
        try:
            regex = re.compile(pattern, flags) if is_regex else None
        except re.error as e:
            return f"Error: Invalid regex pattern: {str(e)}"
        
        # Find matching files
        for root, dirs, files in os.walk(dirpath):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if not fnmatch.fnmatch(file, file_pattern):
                    continue
                
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            match = False
                            if is_regex:
                                match = regex.search(line)
                            else:
                                match = pattern.lower() in line.lower() if not case_sensitive else pattern in line
                            
                            if match:
                                results.append(f"{filepath}:{line_num}: {line.rstrip()}")
                                if len(results) >= max_results:
                                    break
                except:
                    pass
            
            if len(results) >= max_results:
                break
        
        if not results:
            return f"No matches found for pattern: {pattern}"
        
        return f"Found {min(len(results), max_results)} match(es):\n" + "\n".join(results[:max_results])
    except Exception as e:
        return f"Error searching files: {str(e)}"


def get_file_info(
    filepath: Annotated[str, "Path to the file"],
) -> str:
    """Get information about a file (size, modification time, type, etc.).
    
    Args:
        filepath: Path to the file
        
    Returns:
        File information or error message
    """
    try:
        if not os.path.exists(filepath):
            return f"Error: File not found: {filepath}"
        
        stat_info = os.stat(filepath)
        size_kb = stat_info.st_size / 1024
        mod_time = datetime.fromtimestamp(stat_info.st_mtime).isoformat()
        
        # Get file type
        if os.path.isdir(filepath):
            file_type = "Directory"
        else:
            ext = os.path.splitext(filepath)[1]
            file_type = ext if ext else "Unknown type"
        
        info = f"""File Information: {filepath}

Type: {file_type}
Size: {stat_info.st_size} bytes ({size_kb:.2f} KB)
Modified: {mod_time}
Permissions: {oct(stat_info.st_mode)[-3:]}
"""
        return info
    except Exception as e:
        return f"Error getting file info: {str(e)}"


# ============ GIT OPERATIONS ============

def git_status(
    repo_path: Annotated[str, "Path to git repository"] = ".",
) -> str:
    """Get git repository status.
    
    Args:
        repo_path: Path to git repository
        
    Returns:
        Git status output or error message
    """
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            return f"Error: Not a git repository or git not found: {result.stderr}"
        return result.stdout if result.stdout else "Repository is clean (no changes)"
    except Exception as e:
        return f"Error getting git status: {str(e)}"


def git_log(
    repo_path: Annotated[str, "Path to git repository"] = ".",
    max_commits: Annotated[int, "Maximum number of commits to show"] = 10,
) -> str:
    """Get recent git commits.
    
    Args:
        repo_path: Path to git repository
        max_commits: Maximum number of commits
        
    Returns:
        Git log output or error message
    """
    try:
        result = subprocess.run(
            ["git", "log", f"--oneline", f"-{max_commits}"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            return f"Error: Cannot get git log: {result.stderr}"
        return result.stdout if result.stdout else "No commits found"
    except Exception as e:
        return f"Error getting git log: {str(e)}"


def git_diff(
    repo_path: Annotated[str, "Path to git repository"] = ".",
    filepath: Annotated[str, "Specific file to show diff for (optional)"] = "",
) -> str:
    """Get git diff of uncommitted changes.
    
    Args:
        repo_path: Path to git repository
        filepath: Specific file to diff (optional)
        
    Returns:
        Git diff output or error message
    """
    try:
        cmd = ["git", "diff"]
        if filepath:
            cmd.append(filepath)
        
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return f"Error: Cannot get git diff: {result.stderr}"
        
        output = result.stdout
        if len(output) > 5000:
            output = output[:5000] + "\n[... diff truncated ...]"
        
        return output if output else "No changes to show"
    except Exception as e:
        return f"Error getting git diff: {str(e)}"


# ============ FILE OPERATIONS - ADVANCED ============

def create_directory(
    dirpath: Annotated[str, "Path to the directory to create"],
) -> str:
    """Create a directory and any parent directories needed.
    
    Args:
        dirpath: Directory path
        
    Returns:
        Success or error message
    """
    try:
        os.makedirs(dirpath, exist_ok=True)
        return f"Successfully created directory: {dirpath}"
    except Exception as e:
        return f"Error creating directory: {str(e)}"


def delete_file(
    filepath: Annotated[str, "Path to the file to delete"],
) -> str:
    """Delete a file.
    
    Args:
        filepath: Path to the file
        
    Returns:
        Success or error message
    """
    try:
        if not os.path.exists(filepath):
            return f"Error: File not found: {filepath}"
        
        if os.path.isdir(filepath):
            return f"Error: {filepath} is a directory, not a file. Use delete_directory instead."
        
        os.remove(filepath)
        return f"Successfully deleted: {filepath}"
    except Exception as e:
        return f"Error deleting file: {str(e)}"


def delete_directory(
    dirpath: Annotated[str, "Path to the directory to delete"],
    recursive: Annotated[bool, "Delete directory and all contents"] = False,
) -> str:
    """Delete a directory.
    
    Args:
        dirpath: Path to the directory
        recursive: Whether to delete recursively
        
    Returns:
        Success or error message
    """
    try:
        if not os.path.exists(dirpath):
            return f"Error: Directory not found: {dirpath}"
        
        if not os.path.isdir(dirpath):
            return f"Error: {dirpath} is a file, not a directory."
        
        if not recursive:
            os.rmdir(dirpath)
        else:
            import shutil
            shutil.rmtree(dirpath)
        
        return f"Successfully deleted: {dirpath}"
    except Exception as e:
        return f"Error deleting directory: {str(e)}"


def copy_file(
    source: Annotated[str, "Source file path"],
    destination: Annotated[str, "Destination file path"],
) -> str:
    """Copy a file.
    
    Args:
        source: Source file path
        destination: Destination file path
        
    Returns:
        Success or error message
    """
    try:
        if not os.path.exists(source):
            return f"Error: Source file not found: {source}"
        
        # Create destination directory if needed
        dest_dir = os.path.dirname(destination)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)
        
        import shutil
        shutil.copy2(source, destination)
        return f"Successfully copied {source} to {destination}"
    except Exception as e:
        return f"Error copying file: {str(e)}"


def analyze_risk_level(
    threat_name: Annotated[str, "The name or description of the threat"],
    affected_systems: Annotated[int, "Number of affected systems"],
    data_exposure: Annotated[bool, "Whether sensitive data is exposed"],
) -> str:
    """Analyze and rate risk level of a security threat.
    
    Args:
        threat_name: Name of the threat
        affected_systems: Number of affected systems
        data_exposure: Whether data exposure occurred
        
    Returns:
        Risk assessment analysis
    """
    risk_score = 0
    
    # Calculate risk score
    if affected_systems > 1000:
        risk_score += 30
    elif affected_systems > 100:
        risk_score += 20
    elif affected_systems > 10:
        risk_score += 10
    else:
        risk_score += 5
    
    if data_exposure:
        risk_score += 50
    else:
        risk_score += 10
    
    # Determine severity
    if risk_score >= 75:
        severity = "CRITICAL"
    elif risk_score >= 50:
        severity = "HIGH"
    elif risk_score >= 25:
        severity = "MEDIUM"
    else:
        severity = "LOW"
    
    return f"""Risk Assessment for: {threat_name}
Severity: {severity}
Risk Score: {risk_score}/100
Affected Systems: {affected_systems}
Data Exposure: {"Yes" if data_exposure else "No"}
Assessment Date: {datetime.now().isoformat()}

Recommendation: {_get_severity_recommendation(severity)}"""


def get_cve_remediation(
    cve_id: Annotated[str, "CVE identifier (e.g., CVE-2024-1234)"],
    product: Annotated[str, "Affected product name"],
) -> str:
    """Get remediation guidance for a CVE.
    
    Args:
        cve_id: CVE ID
        product: Affected product
        
    Returns:
        Remediation steps
    """
    return f"""CVE Remediation Guidance
CVE ID: {cve_id}
Affected Product: {product}

Immediate Actions:
1. Assess if your organization uses this product
2. Check installed versions against vulnerability bulletin
3. Review logs for exploitation attempts
4. Apply security patches immediately if available
5. If patches unavailable, implement compensating controls

Detection:
- Monitor for relevant attack signatures
- Check for unusual process behavior
- Review network traffic patterns
- Monitor command execution logs

Prevention:
- Enable automatic patch management
- Implement application whitelisting
- Restrict execution privileges
- Maintain configuration baselines
- Conduct regular vulnerability scanning

Note: Visit https://nvd.nist.gov/vuln/detail/{cve_id} for official details."""


def create_security_checklist(
    topic: Annotated[str, "Security topic (e.g., 'web_app', 'network', 'cloud')"],
) -> str:
    """Create a security hardening checklist.
    
    Args:
        topic: Security topic
        
    Returns:
        Security checklist
    """
    checklists = {
        "web_app": [
            "Implement input validation and sanitization",
            "Use prepared statements to prevent SQL injection",
            "Enable security headers (CSP, X-Frame-Options, etc.)",
            "Implement rate limiting and WAF rules",
            "Use HTTPS/TLS with strong ciphers",
            "Implement authentication and session management",
            "Add CSRF tokens to state-changing operations",
            "Implement access controls and authorization",
            "Log security events and monitor for attacks",
            "Regular security testing and code reviews",
        ],
        "network": [
            "Implement network segmentation",
            "Deploy firewall rules and access controls",
            "Monitor network traffic with IDS/IPS",
            "Implement VPN for remote access",
            "Configure secure DNS (DNSSEC, DNS filtering)",
            "Implement DDoS protection",
            "Enable logging and monitoring",
            "Regular vulnerability scanning",
            "Patch management program",
            "Incident response procedures",
        ],
        "cloud": [
            "Enable cloud access security broker (CASB)",
            "Implement identity and access management",
            "Enable MFA for all accounts",
            "Encrypt data in transit and at rest",
            "Configure security groups and network ACLs",
            "Enable audit logging and monitoring",
            "Regular security assessments",
            "Implement backup and disaster recovery",
            "Compliance with cloud security standards",
            "Third-party risk management",
        ],
    }
    
    checklist = checklists.get(topic, checklists["network"])
    items = "\n".join([f"{i+1}. {item}" for i, item in enumerate(checklist)])
    
    return f"""Security Hardening Checklist: {topic.upper()}

{items}

Remember to tailor these items to your specific environment and risk profile."""


def _get_severity_recommendation(severity: str) -> str:
    """Get recommendation based on severity level."""
    recommendations = {
        "CRITICAL": "Immediate action required. Engage incident response team. Implement emergency patches or compensating controls.",
        "HIGH": "Urgent attention needed. Plan emergency maintenance window. Implement interim controls while patches are evaluated.",
        "MEDIUM": "Schedule remediation within 30 days. Implement compensating controls. Monitor for exploitation.",
        "LOW": "Address in regular maintenance cycle. Document and track. Incorporate into standard patch management.",
    }
    return recommendations.get(severity, "Assess and plan appropriate response.")


# Collection of tools for the agent
SECURITY_TOOLS = [
    # Terminal & Execution
    execute_command,
    
    # File Operations
    get_file_contents,
    write_file,
    list_directory,
    create_directory,
    delete_file,
    delete_directory,
    copy_file,
    
    # Search & File Discovery
    find_files,
    grep_search,
    get_file_info,
    
    # Git Operations
    git_status,
    git_log,
    git_diff,
    
    # Security Analysis (Original)
    analyze_risk_level,
    get_cve_remediation,
    create_security_checklist,
]


def get_tools_summary() -> str:
    """Get summary of available tools."""
    return """Available Tools:

TERMINAL & EXECUTION:
1. execute_command - Execute shell commands with timeout and cwd support

FILE OPERATIONS:
2. get_file_contents - Read file contents with line range support
3. write_file - Write or append content to files
4. list_directory - List directory contents (recursive option)
5. create_directory - Create directories recursively
6. delete_file - Delete files
7. delete_directory - Delete directories (with recursive option)
8. copy_file - Copy files

SEARCH & FILE DISCOVERY:
9. find_files - Find files matching glob patterns
10. grep_search - Search for text/regex in files
11. get_file_info - Get file metadata (size, type, permissions, etc.)

GIT OPERATIONS:
12. git_status - Get git repository status
13. git_log - Show recent git commits
14. git_diff - Show uncommitted changes

SECURITY ANALYSIS:
15. analyze_risk_level - Analyze and rate threat risk levels
16. get_cve_remediation - Get CVE remediation guidance
17. create_security_checklist - Create security hardening checklists"""


# ============ Tool Schemas for Structured Tool Calling ============

class ToolParameter(BaseModel):
    """Schema for a tool parameter."""
    name: str
    type: str
    description: str
    required: bool = True
    enum: list[str] | None = None
    default: Any = None


class ToolSchema(BaseModel):
    """Schema for a tool definition."""
    name: str
    description: str
    parameters: list[ToolParameter]
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": [p.model_dump(exclude_none=True) for p in self.parameters]
        }


# Tool Schema Definitions
TOOL_SCHEMAS: dict[str, ToolSchema] = {
    # Terminal & Execution
    "execute_command": ToolSchema(
        name="execute_command",
        description="Execute a shell command and return the output",
        parameters=[
            ToolParameter(name="command", type="string", description="The shell command to execute"),
            ToolParameter(name="timeout", type="integer", description="Timeout in seconds", default=30, required=False),
            ToolParameter(name="cwd", type="string", description="Working directory for command", default=".", required=False),
        ]
    ),
    
    # File Operations
    "get_file_contents": ToolSchema(
        name="get_file_contents",
        description="Read and return the contents of a file with optional line range",
        parameters=[
            ToolParameter(name="filepath", type="string", description="Path to the file to read"),
            ToolParameter(name="start_line", type="integer", description="Starting line (1-indexed)", default=1, required=False),
            ToolParameter(name="end_line", type="integer", description="Ending line (1-indexed, -1 for end)", default=-1, required=False),
        ]
    ),
    "write_file": ToolSchema(
        name="write_file",
        description="Write or append content to a file",
        parameters=[
            ToolParameter(name="filepath", type="string", description="Path to the file to write"),
            ToolParameter(name="content", type="string", description="Content to write to the file"),
            ToolParameter(name="append", type="boolean", description="Append instead of overwrite", default=False, required=False),
        ]
    ),
    "list_directory": ToolSchema(
        name="list_directory",
        description="List files and directories in a path",
        parameters=[
            ToolParameter(name="dirpath", type="string", description="Path to the directory to list", default=".", required=False),
            ToolParameter(name="recursive", type="boolean", description="List recursively", default=False, required=False),
        ]
    ),
    "create_directory": ToolSchema(
        name="create_directory",
        description="Create a directory and any parent directories needed",
        parameters=[
            ToolParameter(name="dirpath", type="string", description="Path to the directory to create"),
        ]
    ),
    "delete_file": ToolSchema(
        name="delete_file",
        description="Delete a file",
        parameters=[
            ToolParameter(name="filepath", type="string", description="Path to the file to delete"),
        ]
    ),
    "delete_directory": ToolSchema(
        name="delete_directory",
        description="Delete a directory",
        parameters=[
            ToolParameter(name="dirpath", type="string", description="Path to the directory to delete"),
            ToolParameter(name="recursive", type="boolean", description="Delete directory and all contents", default=False, required=False),
        ]
    ),
    "copy_file": ToolSchema(
        name="copy_file",
        description="Copy a file",
        parameters=[
            ToolParameter(name="source", type="string", description="Source file path"),
            ToolParameter(name="destination", type="string", description="Destination file path"),
        ]
    ),
    
    # Search & File Discovery
    "find_files": ToolSchema(
        name="find_files",
        description="Find files matching a glob pattern",
        parameters=[
            ToolParameter(name="pattern", type="string", description="Glob pattern (e.g., '**/*.py', '*.json')"),
            ToolParameter(name="dirpath", type="string", description="Starting directory", default=".", required=False),
            ToolParameter(name="max_results", type="integer", description="Maximum results", default=50, required=False),
        ]
    ),
    "grep_search": ToolSchema(
        name="grep_search",
        description="Search for text or regex patterns in files",
        parameters=[
            ToolParameter(name="pattern", type="string", description="Text or regex pattern to search for"),
            ToolParameter(name="dirpath", type="string", description="Directory to search in", default=".", required=False),
            ToolParameter(name="file_pattern", type="string", description="File pattern to search within", default="*", required=False),
            ToolParameter(name="is_regex", type="boolean", description="Treat pattern as regex", default=False, required=False),
            ToolParameter(name="case_sensitive", type="boolean", description="Case-sensitive search", default=False, required=False),
            ToolParameter(name="max_results", type="integer", description="Maximum results", default=50, required=False),
        ]
    ),
    "get_file_info": ToolSchema(
        name="get_file_info",
        description="Get file metadata (size, type, modification time, permissions)",
        parameters=[
            ToolParameter(name="filepath", type="string", description="Path to the file"),
        ]
    ),
    
    # Git Operations
    "git_status": ToolSchema(
        name="git_status",
        description="Get git repository status",
        parameters=[
            ToolParameter(name="repo_path", type="string", description="Path to git repository", default=".", required=False),
        ]
    ),
    "git_log": ToolSchema(
        name="git_log",
        description="Get recent git commits",
        parameters=[
            ToolParameter(name="repo_path", type="string", description="Path to git repository", default=".", required=False),
            ToolParameter(name="max_commits", type="integer", description="Maximum commits to show", default=10, required=False),
        ]
    ),
    "git_diff": ToolSchema(
        name="git_diff",
        description="Get git diff of uncommitted changes",
        parameters=[
            ToolParameter(name="repo_path", type="string", description="Path to git repository", default=".", required=False),
            ToolParameter(name="filepath", type="string", description="Specific file to diff (optional)", default="", required=False),
        ]
    ),
    
    # Security Analysis (Original)
    "analyze_risk_level": ToolSchema(
        name="analyze_risk_level",
        description="Analyze and rate risk level of a security threat",
        parameters=[
            ToolParameter(name="threat_name", type="string", description="The name or description of the threat"),
            ToolParameter(name="affected_systems", type="integer", description="Number of affected systems"),
            ToolParameter(name="data_exposure", type="boolean", description="Whether sensitive data is exposed"),
        ]
    ),
    "get_cve_remediation": ToolSchema(
        name="get_cve_remediation",
        description="Get remediation guidance for a CVE",
        parameters=[
            ToolParameter(name="cve_id", type="string", description="CVE identifier (e.g., CVE-2024-1234)"),
            ToolParameter(name="product", type="string", description="Affected product name"),
        ]
    ),
    "create_security_checklist": ToolSchema(
        name="create_security_checklist",
        description="Create a security hardening checklist",
        parameters=[
            ToolParameter(name="topic", type="string", description="Security topic (e.g., 'web_app', 'network', 'cloud')"),
        ]
    ),
}


def get_tools_schema_for_prompt() -> str:
    """Get formatted tool schemas for including in prompts."""
    schemas = []
    for tool_name, schema in TOOL_SCHEMAS.items():
        schemas.append(f"- {schema.name}: {schema.description}")
    return "\n".join(schemas)


def get_tool_call_instructions() -> str:
    """Get instructions for how the agent should call tools."""
    return """When you need to use a tool, format it as a JSON object like this:

{"tool": "tool_name", "parameters": {"param1": "value1", "param2": "value2"}}

Examples:
{"tool": "execute_command", "parameters": {"command": "ls -la"}}
{"tool": "get_file_contents", "parameters": {"filepath": "/path/to/file"}}
{"tool": "analyze_risk_level", "parameters": {"threat_name": "SQL Injection", "affected_systems": 50, "data_exposure": true}}

After a tool is executed, you will receive the result and should analyze and explain it to the user."""


def validate_tool_call(tool_name: str, parameters: dict) -> tuple[bool, str]:
    """Validate a tool call against its schema.
    
    Args:
        tool_name: Name of the tool
        parameters: Parameters provided
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if tool_name not in TOOL_SCHEMAS:
        return False, f"Unknown tool: {tool_name}"
    
    schema = TOOL_SCHEMAS[tool_name]
    
    # Check required parameters
    for param in schema.parameters:
        if param.required and param.name not in parameters:
            return False, f"Missing required parameter '{param.name}' for tool '{tool_name}'"
    
    # Check parameter types
    for param in schema.parameters:
        if param.name in parameters:
            value = parameters[param.name]
            param_type = param.type.lower()
            
            if param_type == "string" and not isinstance(value, str):
                return False, f"Parameter '{param.name}' must be a string, got {type(value).__name__}"
            elif param_type == "integer" and not isinstance(value, int):
                return False, f"Parameter '{param.name}' must be an integer, got {type(value).__name__}"
            elif param_type == "boolean" and not isinstance(value, bool):
                return False, f"Parameter '{param.name}' must be a boolean, got {type(value).__name__}"
            
            if param.enum and value not in param.enum:
                return False, f"Parameter '{param.name}' must be one of {param.enum}, got {value}"
    
    return True, ""
