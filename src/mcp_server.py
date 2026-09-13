"""Composition root: wires up the MCP server and registers all tools."""
import logging
from server_instance import server
import tools

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)
log.info("Loaded tools: %s", tools.__all__)
