def _live_registry() -> dict[str, object]:
    """Return the registered tool functions keyed by name (side-effect: imports).

    Modules are imported defensively: a tool module that a migration work
    package has already removed (e.g. ``devices`` after WP-14) is skipped
    instead of raising, so this anchor stays valid — and can flip green — at
    the moment the migration completes rather than erroring on the import.
    """
    for _mod in (
        "body",
        "heart",
        "sleep",
        "stress",
        "steps",
        "hydration",
        "activity",
        "devices",
        "nutrition",
        "goals",
        "util",
    ):
        try:
            importlib.import_module(f"mcp_garmin.tools.{_mod}")
        except ImportError:
            continue
    return {f.__name__: f for f in base.get_registered_tools()}