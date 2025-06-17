# Node 1: Scope & Inventory

## Overview

The Scope & Inventory node performs an exhaustive, *static* discovery pass over the **source repository** so that every later node has a complete, precise picture of what must be migrated. Its single responsibility is to return a machine‑readable snapshot of the codebase that captures structure, behaviour, and external surface area while making **no mutations**.

The Scope Node is the first and foundational component of the Codebase Tech Stack Transformer agent. Its primary responsibility is to perform comprehensive static analysis of any full-stack, frontend, or backend web/desktop application repository to extract all prerequisite information needed for accurate technology stack transformation.

## Core Objective

Generate a complete inventory and analysis of the target codebase including file structure, dependencies, code relationships, database schemas, API endpoints, and architectural patterns to enable subsequent nodes to perform accurate stack transformation.

## Architecture

The Scope Node operates as an LLM-orchestrated sub-flow using Gemini with LangChain, coordinating multiple specialized tools and analysis components through structured output generation.

### Primary Components

**Orchestrator**: Central Gemini instance with system prompt defining comprehensive codebase analysis responsibilities and binding to the tools.

**Tool Suite**: Collection of Python functions and terminal command wrappers for file system analysis, code parsing, and information extraction.

**Output Structured Schema**: Predefined data models using Pydantic for consistent, machine-readable analysis results.


## Inputs

* `repo_root` – absolute path to the root of the repository to analyse.

## System Prompt Design
**A comprehensive version of this prompt will be used, this is just a placeholder**

The Gemini orchestrator will be initialized with a system prompt establishing its role as a comprehensive codebase analyzer with the following directives:

- Analyze complete project structure systematically
- Extract all relevant technical information for stack transformation
- Use available tools strategically based on initial project assessment
- Generate structured output for downstream processing
- Handle different project types and technology stacks dynamically

## Tool Specifications

### Root Directory Inspector
**Function**: `inspect_root_directory()`
**Purpose**: Initial project assessment and technology stack detection
**Process**: Executes `ls -la` in project root directory
**Output**: List of files and directories with metadata
**Usage**: First tool called to determine project type and subsequent analysis strategy

### Intelligent Tree Generator
**Function**: `generate_project_tree(exclude_patterns, max_depth)`
**Purpose**: Create comprehensive hierarchical file structure
**Parameters**:
- `exclude_patterns`: List of patterns to exclude (node_modules, .venv, .git, dist, build, __pycache__)
- `max_depth`: Maximum directory depth to traverse (default: 10)
**Process**: Constructs and executes tree command with intelligent exclusions based on detected project type
**Output**: Structured hierarchical representation of project files and directories
**Integration**: Orchestrator determines exclusion patterns based on root directory analysis

### Read File
**Function**: `read_file(file_path)`
**Purpose**: Read the contents of a file
**Process**: Allows Gemini to read the contents of a file.
**Output**: The contents of the file

### Database Schema Analyzer
**Function**: `analyze_database_schemas()`
**Purpose**: Extract database connection information and schema definitions
**Process**:
- Uses a separate instance of Gemini to analyze the database schema using the info from the root directory inspector and the tree generator.
- Searches for database configuration files (knex.js, alembic, migrations, models)
- Parses ORM model definitions
- Extracts connection strings and database types
- Identifies migration files and schema evolution patterns
**Output**: Database schema structure, relationships, and connection metadata
**Supported Formats**: SQL migrations, ORM models, NoSQL schemas, configuration files

### API Endpoint Extractor
**Function**: `extract_api_endpoints()`
**Purpose**: Catalog all API routes and endpoints
**Process**:
- Uses a separate instance of Gemini to analyze the API endpoints using the info from the root directory inspector and the tree generator.
- Parses route definition files (Express routes, Django URLs, Flask blueprints)
- Extracts HTTP methods, paths, and handler functions
- Identifies middleware and authentication patterns
- Maps controllers to route definitions
**Output**: Complete API endpoint inventory with methods, paths, and associated handlers
**Framework Support**: Express, Django, Flask, FastAPI, Spring Boot, and other common frameworks

### Code Structure Analyzer
**Function**: `analyze_code_structure()`
**Purpose**: Extract all functions, classes, variables, and their relationships
**Process**:
- Uses a separate instance of Gemini to analyze the code structure using the info from the root directory inspector and the tree generator.
- Gemini instance uses Abstract Syntax Tree parsing for each supported language
- Identifies function definitions, class declarations, and variable assignments
- Extracts function parameters, return types, and docstrings
- Maps class inheritance relationships and method definitions
**Output**: Comprehensive inventory of code elements with metadata and relationships
**Language Support**: JavaScript, TypeScript, Python, Java, C#, Go, and other common languages

### Call Graph Generator
**Function**: `build_call_graph()`
**Purpose**: Create hierarchical representation of function and method invocations
**Process**:
- Analyzes function calls within each file
- Tracks cross-file function invocations
- Identifies method calls on class instances
- Maps callback and event handler relationships
- Generates directed graph structure
**Output**: Hierarchical call graph showing which functions call which other functions across the entire codebase
**Structure**: File-based hierarchy with function-to-function relationship mappings

### Dependency Graph Builder
**Function**: `build_dependency_graph()`
**Purpose**: Map file-level import and dependency relationships
**Process**:
- Parses import statements and require calls
- Tracks module dependencies from package managers
- Identifies internal file dependencies
- Maps external library usage patterns
- Generates dependency hierarchy
**Output**: Hierarchical dependency graph showing file-to-file and module-to-module relationships
**Coverage**: Internal file dependencies, external package dependencies, and cross-module relationships

### Package Manager Analyzer
**Function**: `analyze_package_dependencies()`
**Purpose**: Extract and categorize external dependencies
**Process**:
- Parses package.json, requirements.txt, pom.xml, go.mod, and other dependency files
- Categorizes dependencies as production, development, or optional
- Extracts version constraints and compatibility information
- Identifies deprecated or security-vulnerable packages
**Output**: Structured dependency inventory with categorization and metadata

## Scope State
The Scope Node maintains a persistent in-memory object named `ScopeState`. It tracks every message, tool outcome, and intermediate artefact generated during analysis and is checkpointed to disk after **each** mutating action so the outer agent can resume work deterministically.

```python
from __future__ import annotations
from pathlib import Path
from time import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class LLMMessage(BaseModel):
    role: str                     # "system" | "user" | "assistant" | "tool"
    content: str                  # raw text
    tool_name: Optional[str] = None
    ts: float = Field(default_factory=time)

class ScopeState(BaseModel):
    # --- Meta --------------------------------------------------------------
    repo_root: Path
    phase: str = "initialised"      # current phase label
    step: str = ""                  # fine-grained step inside the phase
    completed: bool = False

    # --- Conversation history ---------------------------------------------
    conversation: List[LLMMessage] = []

    # --- Tool outputs ------------------------------------------------------
    root_listing: Optional[List[str]] = None
    project_tree: Optional[str] = None
    package_dependencies: Optional[Dict[str, Any]] = None
    code_inventory: Optional[Dict[str, Any]] = None
    call_graph: Optional[Dict[str, Any]] = None
    dependency_graph: Optional[Dict[str, Any]] = None
    api_endpoints: Optional[List[Dict[str, Any]]] = None
    database_schemas: Optional[List[Dict[str, Any]]] = None

    # --- Consolidated result ----------------------------------------------
    analysis: Optional[CodebaseAnalysis] = None
```

Helper API exposed to the orchestrator:

```python
state.append_msg(role, content, tool=None)  # push message & persist
state.set_attr("project_tree", tree_str)   # set value & persist
```

* **Persistence** – `ScopeState.json()` is written to `state/scope_state.json` after every mutation.
* **Rollback** – on node startup the orchestrator attempts `load_state()` and continues from the last incomplete phase.
* **Message storage** – every Gemini request/response and every tool invocation/return is wrapped in an `LLMMessage` and appended to `conversation`.

---

### Detailed LLM Orchestration Sequence

The table below shows the exact execution path, which Gemini instance is used, which tool is invoked, and where the result is stored in `ScopeState`.

| Step | Gemini Instance | Prompt Persona | Tool / Action | ScopeState slot |
|------|-----------------|----------------|---------------|-----------------|
| 0 | PrimaryOrchestrator | `system_prompt_scope` | initialise state, append system & user messages | `conversation` |
| 1 | PrimaryOrchestrator | same | `inspect_root_directory()` | `root_listing` |
| 2 | PrimaryOrchestrator | same | summarise listing & decide next | `conversation` |
| 3 | PrimaryOrchestrator | same | `generate_project_tree()` | `project_tree` |
| 4 | PrimaryOrchestrator | same | `analyze_package_dependencies()` | `package_dependencies` |
| 5 | WorkerGemini-AST | `code-structure-worker` | `analyze_code_structure()` | `code_inventory` |
| 6 | WorkerGemini-CallGraph | `call-graph-worker` | `build_call_graph()` | `call_graph` |
| 7 | WorkerGemini-Deps | `dependency-worker` | `build_dependency_graph()` | `dependency_graph` |
| 8 | WorkerGemini-API | `api-surface-worker` | `extract_api_endpoints()` | `api_endpoints` |
| 9 | WorkerGemini-DB | `db-schema-worker` | `analyze_database_schemas()` | `database_schemas` |
| 10 | PrimaryOrchestrator | same | assemble `CodebaseAnalysis` | `analysis` |
| 11 | PrimaryOrchestrator | same | emit final result to outer agent | — |

**Key Points**
1. **PrimaryOrchestrator** – a long-lived Gemini chat that keeps the full conversation and is responsible for planning and consolidation.
2. **WorkerGemini instances** – short-lived Gemini chats with specialised prompts. They receive only the minimal context slice necessary for their task and return strictly-typed JSON.
3. **Tool invocation plumbing** – the orchestrator emits a JSON tool call, the python wrapper executes, the result is serialised back to Gemini, and both the tool result and follow-up assistant messages are recorded in `ScopeState.conversation`.
4. **Checkpoint granularity** – after each step the orchestrator calls `state.persist()` to guarantee resumability.

#### Pseudocode Sketch

```python
state = load_or_init_state(repo_root)
orchestrator = GeminiChat(system_prompt_scope, memory=state.conversation)

# 0: already recorded system + user messages

# 1: root listing
a = inspect_root_directory(repo_root)
state.set_attr("root_listing", a)
state.append_msg("tool", json.dumps(a), tool="inspect_root_directory")

orchestrator.ask(f"Here is the root listing: ```{a}```\nWhat should we do next?")
state.append_msg("assistant", orchestrator.last_response)

# 2-n: loop until analysis complete
while not state.analysis:
    next_tool = orchestrator.decide_tool()
    result = globals()[next_tool](...)
    state.set_attr(slot_map[next_tool], result)
    state.append_msg("tool", json.dumps(result), tool=next_tool)
    orchestrator.ask(f"Tool {next_tool} output attached.")

# 11: finalise
save_to_markdown(state.analysis, "migration_docs/scope_inventory.md")
```

---

## Orchestration Flow

### Phase 1: Initial Assessment
1. Execute `inspect_root_directory()` to analyze project root
2. Determine project type, primary technology stack, and framework patterns
3. Generate analysis strategy based on detected technologies

### Phase 2: Structure Analysis
1. Call `generate_project_tree()` with intelligent exclusion patterns
2. Execute `analyze_package_dependencies()` to understand external dependencies
3. Run `analyze_code_structure()` to inventory all code elements

### Phase 3: Relationship Mapping
1. Execute `build_call_graph()` to map function invocation relationships
2. Run `build_dependency_graph()` to establish file dependency hierarchy
3. Call `extract_api_endpoints()` to catalog API surface area

### Phase 4: Infrastructure Analysis
1. Execute `analyze_database_schemas()` to understand data layer
2. Perform additional framework-specific analysis based on detected patterns
3. Generate comprehensive analysis summary

## Structured Output Schema

### Primary Output Structure
```python
class CodebaseAnalysis(BaseModel):
    project_metadata: ProjectMetadata
    file_structure: FileStructure
    code_inventory: CodeInventory
    call_graph: CallGraph
    dependency_graph: DependencyGraph
    api_endpoints: List[APIEndpoint]
    database_schemas: List[DatabaseSchema]
    external_dependencies: ExternalDependencies
    analysis_summary: AnalysisSummary
```

### Supporting Data Models
Each component will use detailed Pydantic models to ensure consistent, structured output that subsequent nodes can reliably process.

## Error Handling and Robustness

The orchestrator will implement comprehensive error handling for various scenarios including incomplete projects, permission issues, corrupted files, and unsupported technologies. Partial analysis results will be preserved and marked appropriately for downstream processing.

## Integration Points

The Scope Node output will serve as the foundational input for subsequent architecture analysis and transformation planning nodes. The structured output format ensures compatibility with downstream LLM processing and transformation logic.

## Performance Considerations

Analysis will be optimized for large codebases through parallel processing of independent analysis tasks, intelligent file filtering, and progressive analysis depth based on project complexity.

---