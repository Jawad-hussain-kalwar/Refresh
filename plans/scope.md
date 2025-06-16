# Node 1 Implementation Plan: Scope & Inventory

## Overview
This document provides the detailed implementation plan for **Node 1: Scope & Inventory** - the first node in the single agent codebase migration system. This node serves as the foundational analysis phase that inventories and understands the source codebase before passing control to subsequent nodes in the pipeline.

## Node Architecture Context

### Single Agent Pipeline Position
```
[Node 1: Scope & Inventory] → [Node 2: Golden Master Tests] → [Node 3: Architecture Map] → ...
```

The Scope & Inventory node is the **entry point** of the single agent migration system. It receives the source codebase path and produces a comprehensive inventory that subsequent nodes depend on for their specialized tasks.

### Node Responsibilities
- **Primary Function**: Comprehensive source codebase analysis and inventory generation
- **Input**: Source codebase path, analysis parameters
- **Output**: Structured inventory, dependency mapping, architecture insights
- **Next Node**: Golden Master Test Suite generation

## Node Implementation Strategy

### Internal Node Flow
The node operates through intelligent sub-phases with potential loops and retries:

```
Source Input → Discovery → Tool Selection → Analysis Execution → Validation → Output Generation
     ↑                                                              ↓
     └── Retry Loop (if incomplete or inconsistent results) ←──────┘
```

### Adaptive Analysis Approach
Rather than following rigid steps, this node makes runtime decisions about:
- **Which tools to use** based on detected technologies
- **Analysis depth** based on project complexity and available time  
- **Retry strategies** when initial analysis is incomplete
- **Human intervention** when facing ambiguous patterns

## Project Structure

```
Refresh/
├── main.py                         # Single agent initialization
├── graph.py                        # Complete pipeline graph (8 nodes)
├── state/
│   ├── __init__.py
│   └── agent_state.py              # Shared state across all nodes
├── nodes/
│   ├── __init__.py
│   ├── scope.py                    # Node 1: Scope & Inventory implementation
│   ├── golden_tests.py             # Node 2: Golden Master Test Suite (future)
│   ├── architecture.py             # Node 3: Architecture Map (future) 
│   └── ...                         # Additional nodes (future)
├── tools/
│   ├── __init__.py
│   └── scope/                      # Tools specific to Node 1
│       ├── __init__.py
│       ├── tree.py                 # File system scanning
│       ├── dependency_analyzer.py  # Dependency extraction
│       ├── call_graph.py           # Call graph generation
│       ├── api_detector.py         # API endpoint detection
│       └── db_scanner.py           # Database schema analysis
├── config/
│   ├── __init__.py
│   └── settings.py                 # System-wide configuration
├── utils/
│   ├── __init__.py
│   ├── file_utils.py               # File operations
│   └── logging_utils.py            # Logging configuration
├── migration_docs/                 # Generated outputs from all nodes
│   ├── scope_inventory.md          # Node 1 output
│   ├── test_suite.md               # Node 2 output (future)
│   └── ...                         # Additional node outputs
└── requirements.txt
```

## Node 1 Detailed Implementation

### 1. Agent State Schema (state/agent_state.py)
```python
class MigrationState(TypedDict):
    # Global pipeline state
    source_path: str
    target_platform: Optional[str]
    current_node: str
    pipeline_progress: Dict[str, str]
    
    # Node 1: Scope & Inventory outputs
    repository_info: Dict[str, Any]
    file_inventory: Dict[str, Any]
    dependency_graph: Dict[str, Any]
    architecture_patterns: Dict[str, Any]
    api_endpoints: List[Dict[str, Any]]
    database_schemas: List[Dict[str, Any]]
    scope_analysis_complete: bool
    
    # Future nodes will add their own state fields
    # golden_tests: Dict[str, Any]      # Node 2
    # architecture_map: Dict[str, Any]  # Node 3
    # ...
    
    # Shared across all nodes
    errors: List[Dict[str, Any]]
    warnings: List[str]
    human_interventions: List[Dict[str, Any]]
```

### 2. Node 1 Core Implementation (nodes/scope.py)
```python
class ScopeInventoryNode:
    """Node 1: Comprehensive source codebase analysis and inventory."""
    
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.max_retries = 3
    
    async def execute(self, state: MigrationState) -> MigrationState:
        """Execute scope and inventory analysis with adaptive strategies."""
        
        # Phase 1: Initial Discovery
        discovery_results = await self._discover_project_characteristics(state)
        
        # Phase 2: Adaptive Tool Selection
        analysis_strategy = await self._select_analysis_strategy(discovery_results)
        
        # Phase 3: Parallel Analysis Execution
        analysis_results = await self._execute_analysis_tools(analysis_strategy, state)
        
        # Phase 4: Results Integration and Validation
        integrated_results = await self._integrate_and_validate(analysis_results)
        
        # Phase 5: Gap Analysis and Retry if Needed
        if not self._is_analysis_complete(integrated_results):
            integrated_results = await self._fill_analysis_gaps(integrated_results, state)
        
        # Phase 6: Generate Final Inventory
        inventory_report = await self._generate_inventory_report(integrated_results)
        
        # Update state for next node
        state.update({
            "repository_info": integrated_results["repo_info"],
            "file_inventory": integrated_results["file_inventory"],
            "dependency_graph": integrated_results["dependencies"],
            "architecture_patterns": integrated_results["patterns"],
            "api_endpoints": integrated_results["apis"],
            "database_schemas": integrated_results["databases"],
            "scope_analysis_complete": True,
            "current_node": "golden_tests"  # Next node in pipeline
        })
        
        return state
```

### 3. Specialized Tools for Node 1

#### File System Scanner (tools/scope/tree.py)
```python
@tool
def scan_project_structure(source_path: str, max_depth: int = 10) -> Dict[str, Any]:
    """Comprehensive file system analysis with framework detection."""
    return {
        "file_tree": "...",
        "file_statistics": "...",
        "detected_frameworks": "...",
        "configuration_files": "..."
    }
```

#### Dependency Analyzer (tools/scope/dependency_analyzer.py)
```python
@tool
def analyze_dependencies_comprehensive(source_path: str, detected_languages: List[str]) -> Dict[str, Any]:
    """Multi-language dependency analysis with target platform mapping."""
    return {
        "dependencies": "...",
        "dependency_tree": "...",
        "version_constraints": "...",
        "target_platform_mappings": "..."
    }
```

#### Call Graph Generator (tools/scope/call_graph.py)
```python
@tool
def generate_call_graph_intelligent(source_path: str, languages: List[str]) -> Dict[str, Any]:
    """Adaptive call graph generation using AST parsing and LLM analysis."""
    return {
        "call_graph": "...",
        "entry_points": "...",
        "critical_paths": "...",
        "integration_points": "..."
    }
```

### 4. Node Integration with Pipeline Graph (graph.py)
```python
def create_migration_pipeline_graph() -> StateGraph:
    """Create the complete 8-node single agent pipeline."""
    
    graph = StateGraph(MigrationState)
    
    # Add all 8 nodes
    graph.add_node("scope_inventory", scope_node.execute)
    # graph.add_node("golden_tests", golden_tests_node.execute)  # Future implementation
    # graph.add_node("architecture_map", architecture_node.execute)  # Future implementation
    # ... additional nodes
    
    # Sequential flow with conditional loops
    # graph.add_edge("scope_inventory", "golden_tests")
    # graph.add_edge("golden_tests", "architecture_map")
    # ... additional edges
    
    # Quality gate loops
    # graph.add_conditional_edges(
    #     "quality_gates",
    #     lambda state: "transformation" if state["quality_passed"] else "retry_transformation",
    #     {"transformation": "parallel_verification", "retry_transformation": "automated_transformation"}
    # )
    
    graph.set_entry_point("scope_inventory")
    return graph
```

### 5. Main Application Integration (main.py)
```python
def main():
    """Initialize and run the single agent migration pipeline."""
    
    # Initialize the initial state
    migration_state = MigrationState()
    
    # Create the complete pipeline graph
    pipeline_graph = create_migration_pipeline_graph()
    pipeline_app = pipeline_graph.compile()
    
    # Execute starting from Node 1
    initial_state = {
        "source_path": args.source_path,
        "current_node": "scope_inventory",
        "pipeline_progress": {}
    }
    
    # Run the complete pipeline
    final_state = pipeline_app.invoke(initial_state)
    
    print(f"Migration pipeline completed. Steps perfomed {final_state['pipeline_progress']}")
```

## Node 1 Specific Features

### Intelligent Tool Orchestration
- **Dynamic tool selection** based on detected project characteristics
- **Parallel execution** of compatible analysis tools
- **Fallback strategies** when primary tools fail
- **Progressive refinement** through multiple LLM calls with specialized prompts

### Quality Assurance
- **Cross-validation** between different analysis approaches
- **Completeness checks** to ensure no critical components missed
- **Consistency validation** across different analysis results
- **Automated retry** with different strategies if initial analysis insufficient

### Output Generation
- **Structured inventory reports** in markdown and JSON formats
- **Migration complexity assessments** for downstream nodes
- **Architecture insights** that inform subsequent transformation decisions
- **Dependency mappings** that guide target platform design

## Integration with Subsequent Nodes

### Node 1 → Node 2 Data Flow
- **File inventory** guides test generation priorities
- **Architecture patterns** inform test strategy selection  
- **API endpoints** drive API test creation
- **Database schemas** guide data validation test design

### Node 1 → Node 3 Data Flow
- **Call graphs** inform architecture mapping decisions
- **Dependency relationships** guide component boundary identification
- **Integration points** highlight architectural transition needs

## Current Implementation Priority

**Phase 1:** Core Node 1 implementation
- Basic file scanning and inventory generation
- Simple dependency analysis
- Integration with single agent pipeline structure

**Phase 2:** Advanced Node 1 capabilities  
- Intelligent call graph generation
- Comprehensive API and database analysis
- Advanced framework pattern detection

**Phase 3:** Pipeline integration
- Seamless data flow to Node 2
- Quality gate implementation
- Error handling and retry mechanisms

This approach ensures Node 1 serves as a solid foundation for the entire single agent migration pipeline while maintaining modularity for future enhancements.
