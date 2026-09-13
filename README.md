# MCP Server mit garth-ng

Ein dünner MCP-Server-Layer über der [garth-ng](https://pypi.org/project/garth-ng/)-Library, um eigene Garmin-Connect-Daten einem LLM über das [Model Context Protocol](https://modelcontextprotocol.io) bereitzustellen.

## Projektstruktur

```
mcp-garmin/
├── src/
│   ├── garmin_client.py   # Garth-Login/Session-Handling + Datenzugriff
│   ├── mcp_server.py      # MCP-Server-Definition und Tools
│   ├── main.py             # Einstiegspunkt (startet den Server über stdio)
│   └── explore_sleep.py    # Standalone-Skript zum manuellen Testen der Garth-Anbindung
├── .env.template            # Vorlage für Zugangsdaten
├── .pylintrc
├── requirements.txt
├── LICENSE
└── README.md
```

## Installation

```bash
# Virtuelles Environment anlegen und aktivieren
python3 -m venv venv
source venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt
```

## Zugangsdaten einrichten

```bash
cp .env.template .env
```

Trag in `.env` deine Garmin-Connect-Zugangsdaten ein (`GARMIN_USERNAME`, `GARMIN_PASSWORD`). Beim ersten Start wird damit einmalig eingeloggt und die Session unter `~/.garth` gespeichert — danach wird diese gespeicherte Session wiederverwendet, ohne erneuten Login.

## Nutzung

**MCP-Server starten** (wartet über stdio auf einen Client, z.B. Claude Desktop):

```bash
python src/main.py
```

**Zum manuellen Testen der Garth-Anbindung** (ohne MCP-Protokoll):

```bash
python src/explore_sleep.py
```

**Zum interaktiven Testen des MCP-Servers** mit dem [MCP Inspector](https://github.com/modelcontextprotocol/inspector):

```bash
npx -y @modelcontextprotocol/inspector ./venv/bin/mcp run src/mcp_server.py:server
```

Öffnet einen Browser-Tab mit Inspector-UI, in dem sich die verfügbaren Tools direkt aufrufen lassen.

## Verfügbare Tools

| Tool | Beschreibung |
|---|---|
| `ping` | Health-Check, gibt `"pong"` zurück |
| `get_sleep_summary(target_date)` | Zusammenfassung der Schlafdaten für ein Datum (ISO 8601, `YYYY-MM-DD`): Gesamtschlafzeit, Schlafphasen, Scores, Atemfrequenz u.a. |

## Lizenz

[MIT](LICENSE)
