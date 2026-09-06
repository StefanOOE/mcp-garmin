# mcp-garmin

MCP server for accessing Garmin Connect data.

## Features

- Complete Garmin Connect data access via MCP protocol
- Modular architecture with clear separation of concerns
- Comprehensive test coverage
- Automated CI/CD pipeline

## Installation

```bash
pip install mcp-garmin
```

## Usage

```python
from mcp_garmin.server import mcp

# Register tools with your MCP server
mcp.register_tool(...)
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-garmin.git
cd mcp-garmin

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install in development mode
pip install -e .
```

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Lint
ruff check .

# Type check
mypy .

# Format
ruff format .
```

## Architecture

The project follows a layered architecture:

1. **Tools Layer**: Individual tools for specific Garmin data access
2. **Service Layer**: Business logic facade
3. **Repository Layer**: Data access abstraction
4. **Client Layer**: Garmin API integration

## Available Tools

- Body tools: weight, blood pressure, body battery
- Heart tools: daily heart rate, HRV, resting heart rate
- Sleep tools: sleep stages, detail data, daily summary
- Stress tools: daily/weekly stress, training status, morning readiness
- Activity tools: activities list, details, map
- Steps tools: daily/weekly steps, daily summary
- Hydration tools: daily fluid intake and history
- Device tools: device info and connected devices
- Nutrition tools: nutrition log and nutrition status
- Goal tools: steps goal, weight goal, Garmin fitness scores
- Util tools: user profile and user settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT