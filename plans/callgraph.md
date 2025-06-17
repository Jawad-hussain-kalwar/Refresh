# persist: false
# Call Graph Builder — `build_call_graph()`

## Purpose
`build_call_graph()` produces a *directed* graph of function-to-function and method-to-method invocations as determined by **static analysis**.  This gives later stages insight into runtime execution flow, hotspots, and cross-layer coupling without running the code.

## Naming Consistency
The original function name was `generate_call_graph()`.  We adopt `build_call_graph()` to align with the "builder" pattern used for dependency graphs.  Upstream orchestrator step names will be updated accordingly.

## Inputs
* `code_inventory` — the ParsedFile dictionary emitted by `analyze_code_structure()`.
* Optional flags:
  * `include_builtins` (default False) – whether to include standard-library calls.
  * `collapse_getters` (default True) – drop trivial `<1 line` accessors to reduce noise.

## Internal Ephemeral State
```python
class CallEdge(BaseModel):
    caller: str   # fully-qualified name e.g. "src.utils.parse:parse_args"
    callee: str
    file: str     # path of caller for quick filtering
    line: int
    indirect: bool = False  # True when call site is dynamic / heuristic

class CallGraphState(BaseModel):
    repo_root: Path
    edges: List[CallEdge] = []
    functions_seen: Set[str] = set()
    dynamic_sites: List[str] = []   # descriptions of heuristic edges
    start_ts: float = Field(default_factory=time)
    errors: List[str] = []
```
Persisted to `state/debug/callgraph_<timestamp>.json` when `persist_debug=True`.

## Algorithm Overview
1. **Seed Edges From Inventory**
   * Each `ParsedFile.calls` entry is a *raw* callee string captured during structure analysis.
   * Build a map `fqn → decl` for O(1) existence checks.
   * For every caller → raw callee pair:
     * If callee exists in map ⇒ direct edge.
     * Else mark `indirect=True` and store in `dynamic_sites`.
2. **Language-Specific Refinement Passes**
   * **Python** — import `ast` again, walk `Call` nodes to confirm callee names; heuristically resolve `self.method()` by class scope.
   * **JavaScript/TypeScript** — use `ts-morph` to resolve property access chains (`obj.fn`) to actual declarations when static type info available.
   * **Java/C#** — rely on symbol table dumps (`javap` / Roslyn) to bind method references.
3. **Heuristic Dynamic Call Recovery**
   * Detect common patterns: event listeners (`on("click", handler)`), higher-order callbacks (`map(fn)`), async/await chains.
   * Where static name is recoverable, create edge; otherwise create indirect placeholder `caller → <dynamic>` so metrics can reflect unknowns.
4. **Pruning & Deduplication**
   * Remove self-loops (`f → f`).
   * Collapse identical edges; store `count` attr if multiple occurrences.
   * Apply `collapse_getters` flag.
5. **Return Value**
   * `{ "functions": list(functions_seen), "edges": [edge.dict() for edge in edges] }`  
   * No layout or visualisation performed here.

## Performance Considerations
* Worklist partitioned by language to minimise adapter switches.
* Indirect edges cap: max 1 M; otherwise abort with error to prevent runaway heuristics.
* Pool size heuristics: CPU-bound (AST) + I/O-bound (ts-morph subprocess) balanced via `concurrent.futures.ProcessPoolExecutor`.

## Error Handling
* If refinement pass crashes ⇒ edge marks `indirect=True` and notes error.
* If >10 % functions unresolved, builder returns `success=False` so orchestrator may opt for LLM parsing of call sites.

## LLM Augmentation (Optional)
For highly dynamic languages (Ruby, JS with eval, etc.) an opt-in `use_llm_fallback=True` flag triggers **WorkerGemini-CallGraph** to analyse tricky files:
* Input: file chunk + list of unresolved raw call strings.
* Output: JSON list of `{caller, callee}` edges.
* Merged with existing graph and tagged `source="llm"`.

## Security Notes
* No execution, only static reading.
* Subprocess calls (ts-morph, javap) executed with cwd locked to repo and timeout (30 s).

## Limitations & Roadmap
* Multithreaded / coroutine calls (async Python, Java CompletableFuture) are represented as normal edges; no concurrency semantics captured.
* Polymorphic dispatch results in over-approximation. Future enhancement: inter-procedural type analysis for virtual calls.
* Planned feature: export graph in **gprof2dot** compatible format for existing tooling. 