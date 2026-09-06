"""MCP server exposing Garmin Connect data as tools."""

from __future__ import annotations

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server import MCPServer

from .garmin_service import GarminService
from .repositories import GarminRepository
from .tools.body import *
from .tools.heart import *
from .tools.sleep import *
from .tools.stress import *
from .tools.activity import *
from .tools.steps import *
from .tools.hydration import *
from .tools.devices import *
from .tools.nutrition import *
from .tools.goals import *
from .tools.util import *

# Initialize the repository and service
repository = GarminRepository()
service = GarminService(repository)

# Register all tools with the MCP server
# All tools are now registered via decorators in their respective modules