"""Test for the trivial ping health-check tool."""
from tools.ping import ping


def test_ping_returns_pong():
    """The health-check tool responds without needing any Garmin credentials."""
    assert ping() == "pong"
