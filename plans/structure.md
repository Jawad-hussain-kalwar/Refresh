# persist: false
# Structure Analysis – `analyze_code_structure()`

## Purpose
The purpose of `analyze_code_structure()` is to create an accurate, language-agnostic, static inventory of every **named program element** in a repository. This inventory is the foundation for later graph-building phases (dependency, call-graph, etc.) but is also valuable on its own for documentation and refactoring tools.

## What "Code Structure" Means
* The filesystem path of every source file that is considered part of the "first-party" codebase.
* The programming language detected for that file.
* A syntactic catalogue of top-level declarations **only** (no runtime execution):
  * Modules / namespaces.
  * Classes (name, bases, modifiers, docstring/triple-slash comment if available).
  * Functions and methods (fully-qualified name, parameters, default values, return annotation, decorators / modifiers, docstring).
  * Global variables and constants (name, literal value type, mutability flag if the language exposes it).
  * Export surface (what becomes public via `export`, `module.exports`, `__all__`, public access modifier, etc.).
* A minimal set of ancillary facts required later: import statements, simple call sites (callee name + position). These are collected but **not** resolved or expanded here.
* No inference of types, generics, or control-flow. That belongs in deeper semantic passes.

## Supported Languages
The tool supports any language for which a maintained **Tree-sitter** grammar exists (currently 40+), plus a thin adapter layer for languages with higher-fidelity native parsers.

*Native adapters used in v1*
* Python → `ast` and `inspect` modules for docstring & decorator fidelity.
* TypeScript / JavaScript → `ts-morph` via Node subprocess for accurate type-only imports.
* C# → Roslyn command-line server if `dotnet` found.
* Java → `javaparser` via JVM subprocess.

All other languages fall back to Tree-sitter.

## Internal State Layout (Ephemeral)
```python
class ParsedDecl(BaseModel):
    kind: str  # "class" | "function" | "var" | "module"
    name: str
    fqn: str   # fully-qualified name
    start_line: int
    end_line: int
    extras: Dict[str, Any] = {}

class ParsedFile(BaseModel):
    path: Path
    language: str
    hash: str
    declarations: List[ParsedDecl] = []
    imports: List[str] = []           # raw import/include statements
    calls: List[str] = []             # callee names (unresolved)
    parse_errors: List[str] = []

class StructureState(BaseModel):
    repo_root: Path
    files_total: int = 0
    files_parsed: int = 0
    start_ts: float = Field(default_factory=time)
    parsed_files: Dict[str, ParsedFile] = {}
    errors: List[str] = []
```
The instance lives only for the duration of the tool invocation. If `persist_debug` is passed **True**, the object is dumped to `state/debug/structure_<timestamp>.json` before memory is cleared.

## High-Level Algorithm
1. **Discovery**
   1.1. Enumerate all files under `repo_root` respecting exclusion globs: `vendor`, `node_modules`, `site-packages`, `dist`, `build`, `.git`, `*.min.*`, binary extensions.
   1.2. Detect the language of each file by extension and content sniffing (`filetype` lib).
2. **Parallel Parse Pass** (CPU-bound, multi-process pool)
   2.1. For each file choose parser adapter:
        * If language in `native_adapters` → use that.
        * Else if Tree-sitter grammar available → use Tree-sitter.
        * Else mark file as `unsupported_language` and record warning.
   2.2. Run parser, populate `ParsedFile`. Any exception is caught and recorded in `parse_errors`.
3. **LLM Fallback Pass**
   3.1. Files with non-fatal `parse_errors` are chunked (≤ 4 kB each) and sent to **WorkerGemini-Structure** instance with a JSON-only schema prompt requesting declarations, imports, and call sites.
   3.2. Merge LLM result into `ParsedFile.extras["llm_fallback"]` and clear the error flag.
4. **Consolidation**
   4.1. Merge all `ParsedFile` objects into a single dict keyed by relative path.
   4.2. Update `files_parsed` and calculate summary stats (success rate, error count).
5. **Return Value**
   * `StructureState.parsed_files` serialised to plain JSON so downstream tools do not need Pydantic.

## Tree-sitter Utilisation Details
* A single long-lived Tree-sitter `LanguagePool` is initialised per process, lazily loading grammars as needed.
* Each file is parsed into an AST. A lightweight **node-visitor** walks only top-level statements to avoid full deep traversal cost.
* Queries are written in Tree-sitter's S-expression query language. Examples:
  * Functions: `(function_declaration name: (identifier) @name)`
  * Classes (Python): `(class_definition name: (identifier) @name)`
* The visitor emits `ParsedDecl` objects directly, avoiding extra Python object creation.
* Memory is reclaimed immediately after node visit because only leaf identifiers are stored.

## Worker LLM Design
* Prompt role: _"You are a fail-safe parser. Return strictly valid JSON matching this schema ..."_
* Receives: file chunk + language tag.
* Temperature: 0.1 for determinism.
* Retries: 2 on JSON parse failure.
* Strict rate limit: 5 files/second max.

## Error Handling Strategy
* Any fatal exception bubbles to `StructureState.errors` but never crashes the agent.
* If >20 % of files fail parse → tool returns `success=False` in wrapper result and flags orchestrator to consider rerun with `include_vendors=False` or other mitigations.

## Performance Considerations
* Default worker pool size = `min(8, os.cpu_count())`.
* ParsedFile JSON is compressed with `orjson` before optional persist.
* Hashing uses xxhash for speed.

## Security & Privacy
* LLM fallback never transmits more than 4 kB contiguous source; long sensitive files are skipped.
* All temporary AST objects are cleared with `gc.collect()` before tool end.

## Limitations & Future Enhancements
* Tree-sitter cannot resolve multi-file `partial` classes (C#) – leave stub for phase-2 semantic pass.
* Template languages (ERB, Razor) only partially supported; treat as plain text for now.
* Potential to cache grammar binaries in `~/.cache/ts_langs` to speed up warm start. 