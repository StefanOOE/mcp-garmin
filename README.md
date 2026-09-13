# MCP Server for garth-ng

A thin MCP server layer over the [garth-ng](https://pypi.org/project/garth-ng/) library, exposing your own Garmin Connect data to an LLM via the [Model Context Protocol](https://modelcontextprotocol.io).

## Project Structure

```
mcp-garmin/
├── src/
│   ├── server_instance.py  # Creates the shared MCPServer instance
│   ├── mcp_server.py       # Composition root: wires up the server + tools
│   ├── tools/               # One module per MCP tool
│   │   ├── ping.py
│   │   └── sleep.py
│   ├── garmin_client.py    # Garth login/session handling + data access
│   ├── main.py              # Entry point (starts the server over stdio)
│   └── explore_sleep.py     # Standalone script for manually testing the Garth integration
├── .env.template            # Template for credentials
├── .pylintrc
├── requirements.txt
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

Fill in your Garmin Connect credentials in `.env` (`GARMIN_USERNAME`, `GARMIN_PASSWORD`). On first run, this logs in once and saves the session under `~/.garth` — after that, the saved session is reused without logging in again.

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

## Available Tools

| Tool | Description |
|---|---|
| `ping` | Health check, returns `"pong"` |
| `get_sleep_summary(target_date)` | Summary of sleep data for a date (ISO 8601, `YYYY-MM-DD`): total sleep time, sleep phases, scores, respiration rate, and more |

## License

[MIT](LICENSE)
