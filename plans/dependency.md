# persist: false
# Dependency Graph Builder — `build_dependency_graph()`

## Purpose
`build_dependency_graph()` creates a directed, file-to-file (and optionally module-to-module) graph showing *static inclusion relationships* inside the repository.  An edge A → B means "A directly depends on B" via an import, include, require, load, or similar language construct.

The resulting graph fuels higher-order transforms such as dead-code detection, layer-violation checks, and bundler re-writes.

## Scope of "Dependency"
* **Internal file imports** (`import foo` → `src/foo.py`).
* **Relative path includes** (`require "./utils"`).
* **Package-internal aliases** (`from .subpackage import thing`).
* **Re-export chains** (A imports B and re-exports its names).

External packages (e.g. `react`, `lodash`, `System.Text.Json`) are **not** resolved to source files; they are annotated as `external` nodes so downstream tooling can decide whether to vendor-scan them.

## Internal State Schema (Ephemeral)
```python
class DepEdge(BaseModel):
    src: str   # path or module FQN
    dst: str
    external: bool = False
    line: int  # where import occurred
    raw: str   # original import string

class DepGraphState(BaseModel):
    repo_root: Path
    edges: List[DepEdge] = []
    nodes: Set[str] = set()
    start_ts: float = Field(default_factory=time)
    files_scanned: int = 0
    parse_errors: List[str] = []
```
The object is discarded on completion unless `persist_debug=True`, in which case it is dumped to `state/debug/deps_<timestamp>.json`.

## Inputs
* `code_inventory`: the JSON emitted by `analyze_code_structure()`.
* Optional flags:
  * `include_external` (default False) – attach external package nodes.
  * `language_overrides`: mapping `lang -> custom_resolver` for exotic ecosystems.

## High-Level Algorithm
1. **Initialise graph** with empty node/edge sets.
2. **Iterate inventory**.  For every `ParsedFile`:
   2.1. Add node for the file path.
   2.2. For each raw import string in `imports`:
        * Invoke **resolver** to turn it into a *target path* or *external package name*.
        * Create `DepEdge` with `external` flag accordingly.
3. **Resolver design**
   * **Python / Ruby / PHP** – mimic interpreter search path rules (relative first, then `sys.path` / `include_path`).
   * **Node.js / TS** – leverage `tsc --traceResolution` when available; else replicate Node resolution algorithm (package.json main / index.js / .ts).
   * **Java / C#** – map package names to project folder structure (src/main/java, .csproj Compile Include entries).
   * **Fallback** – treat as external and log.
4. **Post-processing**
   * Collapse duplicate edges.
   * Optionally compute *transitive closure size* to gauge coupling density.
   * Generate quick stats: orphan files, cyclic SCCs, heaviest dependants.
5. **Return Value**
   * `{"nodes": list(nodes), "edges": [edge.dict() for edge in edges]}`
   * Graph is *not* topologically sorted; that is left to consumers.

## Performance Strategies
* Resolution cache keyed by `(import_string, origin_dir)` to avoid expensive repeats.
* Use thread pool for I/O bound checks to filesystem.
* Hard cap 100 K edges; if exceeded, builder aborts with warning so agent can chunk project.

## Error Handling
* Non-resolvable import → mark `external=True` and continue.
* Circular resolution loops break after depth 5 and emit warning.
* If more than 30 % edges unresolved, builder returns `success=False` triggering orchestrator alert.

## Security Considerations
* Path resolution is sandboxed within `repo_root`; any attempt to `..` outwards is blocked and logged.
* No network calls; external packages are left as symbolic nodes.

## Future Enhancements
* Plug-in interface for gradle/maven project graphs.
* Experimental "usage weight" edge attribute counting number of imported symbols.
* Option to emit *layer* metadata (app, domain, infra) via regex mapping config. 