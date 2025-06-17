# Refresh - Codebase Transformation System

## Overview
Refresh is an intelligent **single agent system** that automates codebase transformation and modernization. Built with LangGraph, LangChain, and Google's Gemini AI, it uses **one primary agent** that orchestrates **8 specialized nodes** to analyze source code, understand architecture patterns, and generate production-ready migrated codebases.

## Architecture
The system operates as a **single agent** executing a pipeline of **7 specialized nodes**. After an initial analysis, it works on generating tests and mapping the architecture in parallel before proceeding through the transformation and verification stages. The final output is the 8th item: a fully migrated codebase.

The high-level flow is:
1.  **Scope & Inventory Generation** provides initial insights.
2.  This feeds into both:
    *   **2. Language Agnostic Test Suite**
    *   **3. Architecture Map Generation**
3.  The pipeline then proceeds sequentially from **4. Target Platform Design** through to **7. Re-run Language Agnostic Test Suite**, with built-in quality loops.

Each node can internally loop with multiple LLM calls and specialized tools, but the overall system remains one cohesive agent with shared state and context across all phases.

## Key Features
- **Single Agent Architecture**: One intelligent agent managing the entire transformation pipeline
- **8 Specialized Nodes**: Each node handles a specific phase of the transformation process
- **Intelligent Decision Making**: Uses AI to make runtime decisions about analysis tools and approaches
- **Quality-Driven Flow**: Automatic retry loops and quality gates ensure reliable transformations  
- **Multi-Language Support**: Analyzes and migrates codebases across multiple programming languages and frameworks
- **Production-Ready Output**: Generates complete, tested, and deployable target codebases

## Supported Languages & Frameworks
The agent dynamically detects and adapts to various technologies including:
- **Languages**: Python, JavaScript/TypeScript, Java, C#, Go, Rust, PHP, Ruby
- **Web Frameworks**: React, Vue, Angular, Django, Flask, Express.js, Spring Boot, ASP.NET
- **Databases**: PostgreSQL, MySQL, MongoDB, Redis, SQLite
- **Package Managers**: npm, pip, Maven, Gradle, NuGet, Composer

## Installation & Setup

### Prerequisites
- Python 3.12+
- Git
- Google Gemini API key

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd Refresh

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export GEMINI_API_KEY="your-api-key-here"
```

## Usage
```bash
# Analyze and migrate a local codebase
python main.py --source /path/to/your/project --target python-fastapi

# Run with specific analysis depth
python main.py --source /path/to/project --target react-nextjs --depth comprehensive
```

## Technology Stack
Built with:
- **LangGraph**: Single agent orchestration and node workflow management
- **LangChain**: Tool integration and prompt management
- **Google Gemini**: AI analysis and decision making
- **Tree-sitter**: Multi-language code parsing

## Transformation Pipeline Output

The single agent system produces a complete production-ready transformation through 7 specialized nodes, resulting in the final migrated codebase:

### 1. Scope & Inventory Generation
- Complete project inventory and dependency analysis
- Architecture pattern identification
- Transformation complexity assessment

### 2. Language Agnostic Test Suite  
- Comprehensive behavioral test suite
- UI, API, and integration tests
- Tests that work identically on source and target systems

### 3. Architecture Map Generation
- Detailed architectural documentation
- Component relationship diagrams
- Integration point identification

### 4. Target Platform Design
- Target platform specifications
- Transformation roadmap and strategy
- Dependency mapping and translations

### 5. Automated Transformation
- Complete code transformation to target platform
- Configuration and build file conversion
- Maintaining business logic and functionality

### 6. Quality Evaluation
- Build validation and syntax checking
- Dependency verification
- Quality reports with go/no-go decisions
- **Loop**: Returns to Node 5 if quality gates fail

### 7. Re-run Language Agnostic Test Suite
- Execute golden master tests on transformed code
- Behavioral equivalence verification  
- Divergence detection and reporting
- **Loop**: Returns to Node 5 if tests fail

### 8. Migrated Codebase: Target Stack (Final Output)
- Production readiness validation
- Monitoring and observability setup
- Rollout planning and documentation
- Final deployment package creation

## Current Implementation Status

### ✅ Phase 1: Core Infrastructure & Node 1
- [x] Single agent architecture planning
- [x] LangGraph integration design
- [ ] Node 1 (Scope & Inventory Generation) implementation
- [ ] Basic tool binding framework
- [ ] Shared state management across nodes

### 🔄 Phase 2: Test Foundation (Node 2)
- [ ] Test framework architecture planning
- [ ] Node 2 (Language Agnostic Test Suite) implementation
- [ ] Test execution infrastructure
- [ ] Testing Node Integration with agentic pipeline
- [ ] Quality gate framework (to be implemented in Node 6)

### 📋 Phase 3: Architecture & Planning (Nodes 3-4)
- [ ] Node 3 (Architecture Map Generation) planning
- [ ] Node 3 (Architecture Map Generation) implementation
- [ ] Node 4 (Target Platform Design) planning
- [ ] Node 4 (Target Platform Design) implementation
- [ ] Transformation strategy framework planning
- [ ] Transformation strategy framework implementation

### 📋 Phase 4: Transformation Engine (Nodes 5-6)
- [ ] Node 5 (Automated Transformation) planning
- [ ] Node 5 (Automated Transformation) implementation
- [ ] Node 6 (Quality Evaluation) planning
- [ ] Node 6 (Quality Evaluation) implementation
- [ ] Retry and correction mechanisms
- [ ] Retry and correction mechanisms implementation

### 📋 Phase 5: Verification & Deployment (Node 7 & Final Output)
- [ ] Node 7 (Re-run Language Agnostic Test Suite) planning
- [ ] Node 7 (Re-run Language Agnostic Test Suite) implementation
- [ ] Final Output (Migrated Codebase) preparation planning
- [ ] Final Output (Migrated Codebase) preparation implementation
- [ ] End-to-end pipeline testing
- [ ] End-to-end pipeline testing implementation

## Contributing
This project follows a single agent architecture. When contributing:
- Maintain the single agent design pattern
- Each node should be self-contained but share state
- Use consistent tool binding patterns
- Ensure quality gates and retry mechanisms

## Design Principles
- **Single Agent Orchestration**: One agent manages the entire pipeline with full context
- **Node-Level Modularity**: Each node handles specific responsibilities
- **Quality-Driven Flow**: Continuous validation with automatic retry loops
- **Shared Context**: State and learning maintained across all nodes