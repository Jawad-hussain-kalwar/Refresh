# Refresh - Single Agent Codebase Migration System

## Overview
Refresh is an intelligent **single agent system** that automates codebase migration and modernization. Built with LangGraph, LangChain, and Google's Gemini AI, it uses **one primary agent** that orchestrates **8 specialized nodes** to analyze source code, understand architecture patterns, and generate production-ready migrated codebases.

## Architecture
The system operates as a **single agent** with **8 sequential nodes**:

```
1. Scope & Inventory → 2. Golden Master Tests → 3. Architecture Map → 4. Target Platform Design → 
5. Automated Transformation → 6. Continuous Quality Gates → 7. Parallel Verification → 8. Cut-over & Rollback
```

Each node can internally loop with multiple LLM calls and specialized tools, but the overall system remains one cohesive agent with shared state and context across all phases.

## Key Features
- **Single Agent Architecture**: One intelligent agent managing the entire migration pipeline
- **8 Specialized Nodes**: Each node handles a specific phase of the migration process
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

## Migration Pipeline Output

The single agent system produces a complete production-ready migration through 8 specialized nodes:

### 1. Scope & Inventory
- Complete project inventory and dependency analysis
- Architecture pattern identification
- Migration complexity assessment

### 2. Golden Master Test Suite  
- Comprehensive behavioral test suite
- UI, API, and integration tests
- Tests that work identically on source and target systems

### 3. Architecture Map
- Detailed architectural documentation
- Component relationship diagrams
- Integration point identification

### 4. Target Platform Design
- Target platform specifications
- Migration roadmap and strategy
- Dependency mapping and translations

### 5. Automated Transformation
- Complete code transformation to target platform
- Configuration and build file conversion
- Maintaining business logic and functionality

### 6. Continuous Quality Gates
- Build validation and syntax checking
- Dependency verification
- Quality reports with go/no-go decisions
- **Loop**: Returns to Node 5 if quality gates fail

### 7. Parallel Verification (Master Test Suite)
- Execute golden master tests on transformed code
- Behavioral equivalence verification  
- Divergence detection and reporting
- **Loop**: Returns to Node 5 if tests fail

### 8. Cut-over & Rollback Preparation
- Production readiness validation
- Monitoring and observability setup
- Rollback planning and documentation
- Final deployment package creation

## Current Implementation Status

### ✅ Phase 1: Core Infrastructure & Node 1
- [x] Single agent architecture planning
- [x] LangGraph integration design
- [ ] Node 1 (Scope & Inventory) implementation
- [ ] Basic tool binding framework
- [ ] Shared state management across nodes

### 🔄 Phase 2: Test Foundation (Node 2)
- [ ] Test framework architecture planning
- [ ] Golden Master Test Suite node implementation
- [ ] Test execution infrastructure
- [ ] Testing Node Integration with agentic pipeline
- [ ] Quality gate framework (to be implemented in Node 6)

### 📋 Phase 3: Architecture & Planning (Nodes 3-4)
- [ ] Architecture map node planning
- [ ] Architecture map node implementation
- [ ] Target Platform Design node planning
- [ ] Target Platform Design node implementation
- [ ] Migration strategy framework planning
- [ ] Migration strategy framework implementation

### 📋 Phase 4: Transformation Engine (Nodes 5-6)
- [ ] Automated Transformation node planning
- [ ] Automated Transformation node implementation
- [ ] Continuous Quality Gates node planning
- [ ] Continuous Quality Gates node implementation
- [ ] Retry and correction mechanisms
- [ ] Retry and correction mechanisms implementation

### 📋 Phase 5: Verification & Deployment (Nodes 7-8)
- [ ] Parallel Verification node planning
- [ ] Parallel Verification node implementation
- [ ] Cut-over & Rollback node planning
- [ ] Cut-over & Rollback node implementation
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