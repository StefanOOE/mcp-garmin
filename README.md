# MCP Server for garth-ng

A thin MCP server layer over the [garth-ng](https://pypi.org/project/garth-ng/) library, exposing your own Garmin Connect data to an LLM via the [Model Context Protocol](https://modelcontextprotocol.io).

> **Disclaimer:** This is an unofficial, personal project, not affiliated with or endorsed by Garmin. It uses `garth-ng`, which talks to undocumented, reverse-engineered Garmin Connect endpoints. Use at your own risk, with your own account and credentials.

## Project Structure

```
mcp-garmin/
├── src/
│   ├── config.py            # Central config: env vars, validated on import
│   ├── server_instance.py  # Creates the shared MCPServer instance
│   ├── mcp_server.py       # Composition root: wires up the server + tools
│   ├── tools/               # One module per MCP tool
│   │   ├── ping.py
│   │   └── sleep.py
│   ├── garmin_client.py    # Garth login/session handling + data access
│   ├── main.py              # Entry point (starts the server over stdio)
│   └── explore_sleep.py     # Standalone script for manually testing the Garth integration
├── tests/                    # Mirrors src/, mocks the garth boundary
│   └── tools/
│       ├── test_ping.py
│       └── test_sleep.py
├── .env.template            # Template for credentials and settings
├── .pylintrc
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt     # Adds pytest/pytest-cov on top of requirements.txt
├── LICENSE
└── README.md
```

## Installation

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Setting Up Credentials

```bash
cp .env.template .env
```

Fill in your Garmin Connect credentials in `.env` (`GARMIN_USERNAME`, `GARMIN_PASSWORD`, both required). On first run, this logs in once and saves the session under `~/.garth` — after that, the saved session is reused without logging in again.

Two optional settings, with sensible defaults if omitted:
- `LOG_LEVEL` (default `INFO`) — one of `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- `GARTH_SESSION_DIR` (default `~/.garth`) — where the cached session is stored

## Usage

**Start the MCP server** (waits over stdio for a client, e.g. Claude Desktop):

```bash
python src/main.py
```

**For manually testing the Garth integration** (without the MCP protocol):

```bash
python src/explore_sleep.py
```

**For interactively testing the MCP server** with the [MCP Inspector](https://github.com/modelcontextprotocol/inspector):

```bash
npx -y @modelcontextprotocol/inspector ./venv/bin/mcp run src/mcp_server.py:server
```

Opens a browser tab with the Inspector UI, where the available tools can be called directly.

> **Known issue:** `mcp dev src/mcp_server.py:server` (the CLI's own dev command) currently fails — it spins up an isolated `uv run --with mcp==<version>` environment that's missing the `cli` extras `mcp run` itself needs. The command above works around this by pointing the Inspector directly at this project's own virtual environment instead.

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest -v
pytest --cov=src --cov-report=term-missing  # with coverage
```

Tests mock the `garth` boundary (no real network calls or credentials needed) and live under `tests/`, mirroring the `src/` structure.

## Available Tools

| Tool | Description |
|---|---|
| `ping` | Health check, returns `"pong"` |
| `get_sleep_summary(target_date)` | Summary of sleep data for a date (ISO 8601, `YYYY-MM-DD`): total sleep time, sleep phases, scores, respiration rate, and more |

## License

[MIT](LICENSE)
