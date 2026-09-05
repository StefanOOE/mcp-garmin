# mcp-garmin — Target Architecture (sw-architect, 2026-09-05)

## Current state (audit)

- 11 flat domain modules (body/heart/sleep/...), 40 tools, ~450 LoC, 15 test files, ~800 LoC tests.
- **Anti-pattern 1 — global state + hidden DI:** `client.py` holds a module-level
  `_client` singleton; every tool calls `get_client()`. Tools can only be tested by
  monkeypatching a module global. Violates AGENTS.md DI rule.
- **Anti-pattern 2 — scattered imports:** `import garth` / `from garth.data import ...`
  inside every tool function (30+ occurrences). Fragile against garth API changes;
  one place to patch is not one place to patch in tests.
- **Anti-pattern 3 — Repository rule broken:** `devices.py` calls
  `client.connectapi(...)` (raw endpoint) directly in tool code and swallows
  `except Exception` twice. No repository layer, inconsistent fallback logic.
- **Anti-pattern 4 — dead abstraction:** `_to_dict()` is an identity function
  (`asdict` already returns dicts). Every tool pays a pointless indirection.
- **Smells:** in-function imports, `except Exception` fallbacks with no logging,
  no CI pipeline, no code coverage, `garmin_login.py` outside the package.

## Target architecture

Three layers, strict one-way dependency:

```
tools (MCP layer)          domain (business layer)        data (repository layer)
─────────────────          ──────────────────────          ───────────────────────
server.py (registry)       garmin_service.py               client.py  (garth wiring, token)
<domain>.py — thin         GarminService: typed facade     repositories.py (Repository pattern)
wrappers, docstrings =     over repositories; all business logic:                       ← garth (the only module importing garth)
tool descriptions           fallbacks, field projection,
                             None-handling, error mapping
```

### Package layout (target)

```
src/mcp_garmin/
├── client.py            # garth wiring: build_client(token_dir) -> Client; no globals
├── repositories.py      # GarminRepository (data source abstraction — AGENTS.md rule)
├── garmin_service.py    # GarminService(repository) — all business logic
├── errors.py            # ToolError hierarchy (ToolError, TokenError) + from_garmin()
├── serialization.py     # snake_case projection helpers (sleep fields, device keys)
├── server.py            # MCPServer + registry (decorator-based, no manual list)
└── tools/
    ├── base.py          # tool registry + register() decorator + shared parameter models
    ├── body.py  heart.py  sleep.py  stress.py  steps.py  hydration.py
    ├── activity.py  devices.py  nutrition.py  goals.py  util.py
└── login.py             # garmin_login.py moved into package, exposed as `mcp-garmin-login`
```

### Key decisions

1. **Constructor injection (DI).** `GarminService.__init__(self, repo: GarminRepository)`.
   Tools obtain the service from a single factory:
   `server.py` builds one `GarminService(build_client())` at startup and passes it to
   tool factories. No module-level singletons; tests construct
   `GarminService(FakeGarminRepository())` directly.
2. **Repository pattern (AGENTS.md data-source rule).** All garth access lives in
   `GarminRepository`. Methods mirror domain reads: `weight(day)`, `weight_history(end, days)`,
   `daily_stress(end, period)`, `activity_list(limit, start)`, `device_info()`, ...
   Raw `connectapi()` calls (devices) are repository-internal; tools never see them.
3. **Registry pattern replaces manual `_ALL_TOOLS` list.** `register(mcp, name)` decorator
   in `tools/base.py` — adding a tool is one decorator, no server.py edit.
   `server.py` keeps exactly: MCPServer instance + import of tool modules + `main()`.
4. **Facade for business logic.** `GarminService` holds: device fallback logic
   (deviceinfo → profile, *with logging*, no bare `except Exception`),
   sleep field projection, `None → {}` / `None → []` normalization.
   Tools are ≤5-line pass-throughs: `return service.weight(day=day)`.
5. **Error cascade in one place.** `errors.py`: `ToolError` (base), `TokenError` (subclass).
   `GarminRepository` wraps every garth call with a single `from_garmin(exc)` mapper.
   Tools re-raise `ToolError` untouched; MCP layer translates to tool errors.
6. **Type hints end-to-end.** Tool params: `date: str | None = None` with
   `Annotated[..., Field(description=...)]` so MCP schemas carry real descriptions.
   Repository return types: `dict[str, Any]` (garth dataclass → dict) — keep it
   honest, don't invent per-endpoint TypedDicts (YAGNI; garth-ng is alpha).
7. **Config via env.** `GARMIN_TOKEN_DIR` (default `~/.garth`) read in `client.py` only.
   No hardcoded secrets, no globals.

### Non-goals (YAGNI — keep KISS)

- No per-endpoint Pydantic response models (garth-ng 2.0.0a1 is alpha; dict pass-through stays).
- No caching layer, no async, no plugin system, no HTTP mode (stdio MCP only).
- `garmin_login.py` is moved, not re-architected (one-shot script).
- Tool names, signatures and docstrings stay **byte-compatible** — the MCP tool
  surface is a public contract consumed by other agents. Zero renames.

## Testing architecture (for sw-qa)

- **Unit (domain):** `tests/unit/` — `GarminService` against `FakeGarminRepository`
  (in-memory, deterministic; no MagicMock for the repository itself — a real fake class).
  Coverage targets: fallback paths, None-normalization, error mapping, projection.
  ≥90% line coverage on `garmin_service.py` + `errors.py` + `serialization.py`.
- **Repository (thin):** `tests/repository/` — `GarminRepository` against a mocked
  garth client (MagicMock OK here; this is the boundary layer).
- **Integration (opt-in):** `tests/integration/` — real `~/.garth` token; marked
  `@pytest.mark.integration`, excluded from CI by default, runnable via
  `pytest -m integration` on the dev box. Replaces today's "verified 2026-09-01"
  comments as the source of fixture truth.
- **Contract (regression):** `tests/contract/test_tool_surface.py` — asserts the
  registered tool set equals the frozen list (names, params, required flags) so
  refactors cannot silently change the MCP surface.
- Fixtures: keep `tests/fixtures/*.json` with the real captured payloads (move out of
  conftest.py); conftest shrinks to shared fake-repository wiring.
- CI (GitHub Actions, for sw-developer): ruff check + ruff format + mypy (service/data
  layers only) + pytest (unit+repo+contract) on push/PR to main.

## Work packages (kanban)

| # | Package | Owner | Scope | Depends |
|---|---------|-------|-------|---------|
| W1 | Core layers | sw-developer | `errors.py`, `client.py` (build_client, env config), `repositories.py`, `garmin_service.py`, `serialization.py` + unit tests for service | — |
| W2 | Tool migration | sw-developer | `tools/base.py` registry + all 11 tool modules as thin wrappers; new `server.py`; delete old flat modules; tool-surface contract test; keep garmin_login working via `mcp-garmin-login` | W1 |
| W3 | Quality gates | sw-qa | test reorg (unit/repository/integration/fixtures), ≥90% coverage gates, contract test expansion | W1 |
| W4 | CI pipeline | sw-developer | GitHub Actions: ruff, format, mypy (2 layers), pytest, coverage upload; `.github/workflows/ci.yml` | W1 |
| W5 | Verification & docs | sw-qa | integration run against real token, ruff/mypy green, README updated (new layout, env var, login command), coverage report | W2, W3, W4 |
| W6 | Merge & release | sw-pm | review all PRs, merge to main in order, tag v0.2.0, update Hermes skill/tool list | W5 |

**Quality gates (all packages):** `ruff check` + `ruff format --check` clean;
functions ≤30 lines; no `except Exception` outside `errors.py`/`repositories.py`;
no module-level mutable state; no in-function `import garth` outside `repositories.py`.