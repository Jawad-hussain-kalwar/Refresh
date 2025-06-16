# Basic Tools Implementation Plan

## Overview
This document outlines the foundational tools that will be available to all nodes in the agentic codebase migration system. These tools provide essential file system, terminal, and text processing capabilities that agents can use to explore, analyze, and understand codebases.

## Core Principle
All basic tools are designed to be **safe**, **informative**, and **agentic-friendly** - providing rich context and metadata that agents can use for intelligent decision making.

## Tool Categories

### 1. File System Operations

#### 1.1 File Reading Tools
```python
@tool
def read_file(file_path: str, start_line: Optional[int] = None, end_line: Optional[int] = None) -> Dict[str, Any]:
    """
    Read file contents with optional line range.
    Returns content, encoding, file size, and metadata.
    """

@tool
def read_file_with_context(file_path: str, target_line: int, context_lines: int = 5) -> Dict[str, Any]:
    """
    Read specific lines with surrounding context.
    Useful for focused code analysis.
    """

@tool
def peek_file_structure(file_path: str, max_lines: int = 50) -> Dict[str, Any]:
    """
    Quick file overview - beginning, middle, end snippets.
    Perfect for agents to understand file purpose without reading everything.
    """
```

#### 1.2 File Writing Tools
```python
@tool
def write_file(file_path: str, content: str, create_dirs: bool = True) -> Dict[str, Any]:
    """
    Write content to file with directory creation option.
    Returns operation status and file metadata.
    """

@tool
def append_to_file(file_path: str, content: str) -> Dict[str, Any]:
    """
    Append content to existing file.
    Useful for building reports incrementally.
    """

@tool
def create_file_from_template(template_path: str, target_path: str, variables: Dict[str, str]) -> Dict[str, Any]:
    """
    Create files from templates with variable substitution.
    Useful for generating standardized documentation.
    """
```

#### 1.3 Directory Operations
```python
@tool
def list_directory(dir_path: str, recursive: bool = False, max_depth: int = 3, include_hidden: bool = False) -> Dict[str, Any]:
    """
    List directory contents with metadata.
    Returns file types, sizes, modification dates, and permissions.
    """

@tool
def create_directory(dir_path: str, parents: bool = True) -> Dict[str, Any]:
    """
    Create directory with parent creation option.
    """

@tool
def get_directory_stats(dir_path: str) -> Dict[str, Any]:
    """
    Get comprehensive directory statistics.
    File counts by type, total size, last modified, etc.
    """
```

### 2. Search and Discovery Tools

#### 2.1 Content Search
```python
@tool
def search_in_files(pattern: str, dir_path: str, file_extensions: List[str] = None, 
                   case_sensitive: bool = False, max_results: int = 100) -> Dict[str, Any]:
    """
    Search for text patterns across files.
    Returns matches with file paths, line numbers, and context.
    """

@tool
def find_files_by_name(name_pattern: str, dir_path: str, recursive: bool = True) -> List[Dict[str, Any]]:
    """
    Find files by name pattern.
    Supports glob patterns and regex.
    """

@tool
def find_files_by_content(content_pattern: str, dir_path: str, file_types: List[str] = None) -> List[Dict[str, Any]]:
    """
    Find files containing specific content patterns.
    Returns file paths with matching line previews.
    """
```

#### 2.2 Code-Specific Search
```python
@tool
def find_function_definitions(function_name: str, dir_path: str, languages: List[str] = None) -> List[Dict[str, Any]]:
    """
    Find function/method definitions across multiple languages.
    Returns definitions with signatures and documentation.
    """

@tool
def find_class_definitions(class_name: str, dir_path: str, languages: List[str] = None) -> List[Dict[str, Any]]:
    """
    Find class definitions with inheritance information.
    """

@tool
def find_import_statements(module_name: str, dir_path: str) -> List[Dict[str, Any]]:
    """
    Find import/include statements for specific modules.
    Useful for dependency analysis.
    """
```

### 3. Terminal and Command Execution

#### 3.1 Safe Command Execution
```python
@tool
def execute_command(command: str, working_dir: str = None, timeout: int = 30, 
                   capture_output: bool = True) -> Dict[str, Any]:
    """
    Execute terminal commands safely with timeout.
    Returns stdout, stderr, exit code, and execution metadata.
    
    Safety features:
    - Command whitelist/blacklist
    - Timeout protection
    - Working directory isolation
    - Output size limits
    """

@tool
def execute_read_only_command(command: str, working_dir: str = None) -> Dict[str, Any]:
    """
    Execute read-only commands (ls, cat, grep, etc.).
    Additional safety for commands that don't modify system.
    """
```

#### 3.2 Common Command Shortcuts
```python
@tool
def get_system_info() -> Dict[str, Any]:
    """
    Get system information (OS, architecture, available tools).
    Helps agents adapt to different environments.
    """

@tool
def check_command_availability(commands: List[str]) -> Dict[str, bool]:
    """
    Check if specific commands/tools are available.
    Enables intelligent tool selection.
    """

@tool
def get_environment_variables(var_names: List[str] = None) -> Dict[str, str]:
    """
    Get environment variables (filtered for security).
    """
```

### 4. Text Processing Tools

#### 4.1 Content Analysis
```python
@tool
def analyze_text_file(file_path: str) -> Dict[str, Any]:
    """
    Analyze text file characteristics.
    Returns encoding, line count, character count, language detection.
    """

@tool
def extract_structured_data(file_path: str, data_type: str) -> Dict[str, Any]:
    """
    Extract structured data from files (JSON, YAML, XML, CSV).
    Returns parsed data with validation information.
    """

@tool
def detect_file_type(file_path: str) -> Dict[str, Any]:
    """
    Detect file type and characteristics.
    Returns MIME type, programming language, framework hints.
    """
```

#### 4.2 Content Manipulation
```python
@tool
def extract_lines(file_path: str, line_numbers: List[int]) -> Dict[str, Any]:
    """
    Extract specific lines from file.
    Useful for focused analysis.
    """

@tool
def replace_in_file(file_path: str, search_pattern: str, replacement: str, 
                   preview_only: bool = True) -> Dict[str, Any]:
    """
    Replace text in file with preview option.
    Returns what would be changed before actually changing.
    """
```

### 5. Git and Version Control Tools

#### 5.1 Repository Information
```python
@tool
def get_git_status(repo_path: str) -> Dict[str, Any]:
    """
    Get git repository status.
    Returns branch info, modified files, commit info.
    """

@tool
def get_git_log(repo_path: str, max_commits: int = 10) -> List[Dict[str, Any]]:
    """
    Get recent git commit history.
    Returns commit hashes, messages, authors, dates.
    """

@tool
def get_git_branches(repo_path: str) -> Dict[str, Any]:
    """
    Get all git branches with current branch info.
    """
```

#### 5.2 File History
```python
@tool
def get_file_git_history(file_path: str, repo_path: str) -> List[Dict[str, Any]]:
    """
    Get git history for specific file.
    Returns commits that modified the file.
    """

@tool
def get_git_blame(file_path: str, repo_path: str) -> Dict[str, Any]:
    """
    Get git blame information for file.
    Returns line-by-line authorship information.
    """
```

### 6. Metadata and Analysis Tools

#### 6.1 File Metadata
```python
@tool
def get_file_metadata(file_path: str) -> Dict[str, Any]:
    """
    Get comprehensive file metadata.
    Size, dates, permissions, checksums, etc.
    """

@tool
def calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """
    Calculate file hash for integrity checking.
    """
```

#### 6.2 Project Analysis
```python
@tool
def detect_project_type(dir_path: str) -> Dict[str, Any]:
    """
    Detect project type and characteristics.
    Returns framework, language, build system information.
    """

@tool
def analyze_project_structure(dir_path: str) -> Dict[str, Any]:
    """
    Analyze project directory structure.
    Returns patterns, conventions, potential issues.
    """
```

## Implementation Architecture

### Tool Base Class
```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel

class ToolResult(BaseModel):
    success: bool
    data: Any
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}
    execution_time: float
    
class BasicTool(ABC):
    """Base class for all basic tools"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        
    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Execute the tool with given parameters"""
        pass
        
    def validate_params(self, **kwargs) -> bool:
        """Validate parameters before execution"""
        return True
        
    def get_help(self) -> str:
        """Return tool help/documentation"""
        return self.__doc__ or "No documentation available"
```

### Safety and Security Features

#### 1. Path Validation
```python
def validate_path(path: str, base_path: str = None) -> bool:
    """
    Validate file paths to prevent directory traversal attacks.
    Ensures paths are within allowed directories.
    """
```

#### 2. Command Filtering
```python
ALLOWED_COMMANDS = {
    "read_only": ["ls", "cat", "grep", "find", "head", "tail", "wc"],
    "analysis": ["git", "npm", "pip", "mvn", "gradle"],
    "system": ["which", "whereis", "uname", "whoami"]
}

FORBIDDEN_COMMANDS = ["rm", "del", "format", "shutdown", "reboot"]
```

#### 3. Resource Limits
```python
LIMITS = {
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "max_command_timeout": 60,  # 60 seconds
    "max_output_size": 1024 * 1024,  # 1MB
    "max_search_results": 1000
}
```

### Error Handling and Resilience

#### 1. Graceful Degradation
- Tools continue operating with reduced functionality when some features fail
- Partial results returned with clear indication of what failed
- Alternative approaches suggested when primary method fails

#### 2. Comprehensive Error Reporting
```python
class ToolError(Exception):
    def __init__(self, message: str, error_type: str, recoverable: bool = True):
        self.message = message
        self.error_type = error_type  # "permission", "not_found", "timeout", etc.
        self.recoverable = recoverable
        super().__init__(message)
```

### Integration with Agentic System

#### 1. Tool Discovery
```python
@tool
def list_available_tools(category: str = None) -> Dict[str, Any]:
    """
    List all available tools with descriptions.
    Helps agents discover and select appropriate tools.
    """
```

#### 2. Tool Recommendations
```python
@tool
def suggest_tools_for_task(task_description: str) -> List[Dict[str, Any]]:
    """
    Suggest appropriate tools for a given task.
    Uses LLM reasoning to match tasks with tools.
    """
```

#### 3. Execution Context
- All tools maintain execution context for better error reporting
- Tools can access shared state for coordination
- Execution history maintained for debugging and optimization

## Testing Strategy

### 1. Unit Tests
- Individual tool functionality
- Parameter validation
- Error handling scenarios
- Security boundary testing

### 2. Integration Tests
- Tool combinations and workflows
- Cross-platform compatibility
- Performance under load
- Security vulnerability testing

### 3. Agent Testing
- Tools used by actual agents
- Workflow efficiency
- Error recovery patterns
- Resource usage patterns

## Monitoring and Observability

### 1. Tool Usage Analytics
- Track which tools are used most frequently
- Identify performance bottlenecks
- Monitor error patterns
- Optimize tool selection strategies

### 2. Performance Metrics
- Execution times
- Resource usage
- Success/failure rates
- Agent satisfaction scores

This comprehensive basic tools system provides the foundation for all agentic operations, ensuring agents have reliable, safe, and efficient access to system capabilities while maintaining security and observability.
