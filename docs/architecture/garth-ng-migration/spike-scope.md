# Spike S2 — Tool-Fläche & Migrations-Strategie (Scope)

- **Card:** t_d1a88188 (S2) — Parent: S1 = t_7756ff1b, Feature = t_74b23096
- **Author:** sw-projectmanager — 2026-09-11
- **Basis:** S1-Mapping `spike-api-mapping.md` (Commit `2c3a516`, Runs #49/#51 live-verifiziert) + Konzept `concept.md` (`db4968f`, `concept-approved` 2026-09-10 SS) + Repo-Analyse (`main` = `6a49b8d`, `feature/garth-ng-compat` = `2c3a516`)

---

## 0. Ergebnis (TL;DR)

1. **Tool-Fläche = 40 Tools** (nicht 39). Der Normanker ist der Contract-Test `tests/contract/test_tool_surface.py`, der genau 40 Tools mit Signatur + Return-Shape pinnt. Die "39" in Konzept/Constraints ist Doku-Drift (bereits im Architect-Review markiert).
2. **Basis: `feature/garth-ng-compat`** (User-Entscheidung, bestätigt): Diff zu `main` umfasst nur 4 Code-Dateien (`pyproject.toml`, `client.py`, `login.py`, `tools/sleep.py`) + 2 Doku-Dateien (623+/44−); Tool-Fläche byte-identisch (AST-geprüft, 0 Signature-Diffs). Auth + Sleep sind schon garth-ng — das Kernproblem ist dort gelöst.
3. **Drops: 2 Tools** — `get_connected_devices`, `get_device_info` (Device-Domain = einzige echte Lücke, S1 live: kein ng-Accessor, alle Endpunkt-Varianten 404, `deviceinfo.py` leer). → **Ziel-Fläche: 38 Tools.**
4. **Kein sonstiger Feature-Verlust:** 11× 1:1 + 18× Remap + 8× Endpoint-Fallback (alle `connectapi`-Pfade live 200) + 1× Shape-Drift (`get_garmin_scores`, Dataclass-Patch, kein Drop).
5. **Hermes-MCP:** keine statische Tool-Allowlist in `config.yaml` (Registrierung via stdio-Handshake, `@register`-Registry) → Drops erfordern **kein** Config-Change; der Contract-Test ist die zu synchronisierende Grenze. README "Available Tools" muss die Device-Zeile verlieren.

---

## 1. Bestandsaufnahme — Tool-Fläche (main = `6a49b8d`, garth 0.x)

Registry: `server.py` iteriert über `@register` (Decorator über `@_handle_garmin_error`), `tools/base.py`. **40 Tools** (AST-geprüft; identisch auf `feature/garth-ng-compat`):

| # | Tool | Params | Return | Datei |
|---|---|---|---|---|
| 1 | `get_activities` | `end=None, days=7` | `list[dict]` | activity.py |
| 2 | `get_activity_detail` | `activity_id` | `dict` | activity.py |
| 3 | `get_activity_map` | `activity_id` | `dict` | activity.py |
| 4 | `get_fitness_activities` | `end=None, days=7` | `list[dict]` | activity.py |
| 5 | `get_personal_records` | — | `list[dict]` | activity.py |
| 6 | `get_personal_record_types` | — | `list[dict]` | activity.py |
| 7 | `get_body_weight` | `day=None` | `dict` | body.py |
| 8 | `get_weight_history` | `end=None, days=7` | `list[dict]` | body.py |
| 9 | `get_blood_pressure` | `day=None` | `dict` | body.py |
| 10 | `get_body_battery` | `day=None` | `list[dict]` | body.py |
| 11 | `get_body_battery_stress` | `day=None` | `dict` | body.py |
| 12 | `get_body_battery_stress_history` | `end=None, days=7` | `list[dict]` | body.py |
| 13 | `get_daily_heart_rate` | `day=None` | `list[dict]` | heart.py |
| 14 | `get_hrv` | `day=None` | `list[dict]` | heart.py |
| 15 | `get_resting_heart_rate` | `day=None` | `dict` | heart.py |
| 16 | `get_sleep` | `day=None` | `list[dict]` | sleep.py |
| 17 | `get_sleep_detail` | `day=None` | `dict` | sleep.py |
| 18 | `get_sleep_summary` | `day=None` | `dict` | sleep.py |
| 19 | `get_connected_devices` | — | `list[dict]` | devices.py |
| 20 | `get_device_info` | `device_id` | `dict` | devices.py |
| 21 | `get_steps_goal` | — | `dict` | goals.py |
| 22 | `get_weight_goal` | — | `dict` | goals.py |
| 23 | `get_garmin_scores` | — | `dict` | goals.py |
| 24 | `get_nutrition_log` | `day=None` | `list[dict]` | nutrition.py |
| 25 | `get_nutrition_status` | `day=None` | `dict` | nutrition.py |
| 26 | `get_daily_steps` | `day=None` | `dict` | steps.py |
| 27 | `get_weekly_steps` | `start_date=None` | `list[dict]` | steps.py |
| 28 | `get_daily_summary` | `day=None` | `dict` | steps.py |
| 29 | `get_daily_summary_history` | `end=None, days=7` | `list[dict]` | steps.py |
| 30 | `get_daily_hydration` | `day=None` | `dict` | hydration.py |
| 31 | `get_hydration_history` | `end=None, days=7` | `list[dict]` | hydration.py |
| 32 | `get_daily_stress` | `day=None` | `list[dict]` | stress.py |
| 33 | `get_weekly_stress` | `start_date=None` | `list[dict]` | stress.py |
| 34 | `get_training_status_daily` | `day=None` | `dict` | stress.py |
| 35 | `get_training_status_weekly` | `start_date=None` | `dict` | stress.py |
| 36 | `get_training_status_monthly` | `start_date=None` | `dict` | stress.py |
| 37 | `get_training_readiness` | `day=None` | `dict` | stress.py |
| 38 | `get_morning_readiness` | `day=None` | `dict` | stress.py |
| 39 | `get_user_profile` | — | `dict` | util.py |
| 40 | `get_user_settings` | — | `dict` | util.py |

Units/Shape-Contract (unverändert, pinnt `test_tool_surface.py`): snake_case, ISO-8601-Timestamps, Gewicht in Gramm, `camel_to_snake_dict` via `serialization.py`.

---

## 2. Basis-Entscheidung: `feature/garth-ng-compat` (bestätigt)

User-Entscheidung auf t_74b23096 (2026-09-10): Basis = `feature/garth-ng-compat`. S2 bestätigt mit Daten:

| Kriterium | Befund |
|---|---|
| Diff-Größe | 6 Files, 623+/44−; Code nur `pyproject.toml` (+`garth-ng`), `client.py`, `login.py`, `tools/sleep.py` |
| Tool-Fläche | **identisch** zu main (40/40, 0 Signatur-Diffs, AST-geprüft) → keine Konflikt-Overlay-Risiken auf `tools/*` |
| Stand login+sleep | schon garth-ng: SSO-Login, `refresh_token()` (ohne SSO, umgeht 429), `GARTH_HOME`-Persistenz; Sleep auf `SleepData`/`DailySleepData` — live verifiziert (n=1, Run #49) |
| Rest (36 Tools) | Legacy-Klassen-Imports (z.B. `Activities`, `NutritionLog`, `ConnectedDevices`) — genau der Phase-2-Arbeitsumfang, noch nicht angefasst |
| Karte t_a90d15d9 | `ready`, unassigned; Run #44 **reclaimed** (stale lock `thinkcentre:43052`, non-local host, 2026-09-10), kein WIP auf dem Branch, kein Assignee → **kein Konflikt-Risiko**; ihr Scope (Rest der `tools/*` mappen) wird von den Phase-2-Work-Packages übernommen — Karte kann dann closed/cancelled werden |
| main | frozen (`6a49b8d`), garth 0.x; Migration von main bräuchte login+sleep zuerst neu = Doppelarbeit ohne Vorteil |

**Konsequenz:** Phase-2-Branches bauen auf `feature/garth-ng-compat`; `main` bleibt bis zum finalen Merge (Phase 7, PM) unverändert.

---

## 3. Drops & Rettung — priorisiert nach Nutzwert

**Rette zuerst (hohes Query-Volumen im Hermes-Stack):** Sleep (16–18), Heart/HRV (13–15), Stress/Training/Readiness (32–38), Daily-Summary (28–29), Activity (1–5), Steps (26–27), Body/Weight (7–12) — **alle** liefern live Daten (1:1 oder Remap, S1 verifiziert). Kein einziger dieser Tools fällt raus.

| Tool | Entscheidung | Begründung |
|---|---|---|
| `get_connected_devices` | **DROP** | Keine ng-Domain (leere `deviceinfo.py`), alle connectapi-Varianten 404 (Run #49/#51). Geringer Nutzwert (Device-Queries selten via LLM); leere Liste verwirrt den Client mehr als sie hilft (User-Regel: leere Tools entfernen). |
| `get_device_info` | **DROP** | Wie oben; `device_id`-Param wäre zudem nicht bedienbar (ng-Endpoint nicht pro-Device-parametrierbar). |
| `get_garmin_scores` | **RETTE (Fix)** | Shape-Drift: `GarminScoresData` bricht an `hill_score=None` (erwartet `int`). Fix = Dataclass-Patch `hill_score: int \| None = 0` (zentral, kein Tool-Logik-Change). Fitness-Scores = häufig genutzt. |
| 8× Endpoint-Fallback (PR ×2, blood_pressure, steps/weight goal, nutrition ×2, activity_map) | **RETTE** | Alle Pfade live 200 mit echten Daten (n=2…51, Run #49 + Spot-Check #51) — exakte Pfade in S1 §3. |
| `get_activities` | **RETTE (Signatur-Change)** | Siehe Open-Item 7. |

**Ziel-Fläche: 40 − 2 = 38 Tools.**

---

## 4. Constraint-Check: Hermes-MCP-Registrierung & Docs-Sync

**Hermes-Config** (`~/.hermes/config.yaml`):

```yaml
mcp-garmin:
  command: /home/ss/src/mcp-garmin/.venv/bin/python
  args: [-m, mcp_garmin]
```

- **Keine statische Tool-Allowlist** — der Server registriert seine Tools dynamisch via MCP-stdio-Handshake aus der `@register`-Registry. Drops/Changes erfordern **keine** `config.yaml`-Änderung.
- Die Constraint-Formulierung "39 Tools registriert" ist in zwei Punkten zu korrigieren: (a) die Zahl ist **40** (Contract-Test + S1-Probe `tool_map.json` = 40 Einträge); (b) die Bindung ist nicht die Config, sondern **`tests/contract/test_tool_surface.py`** (pinnt exakt Name + Signatur + Return-Shape aller 40).
- **Änderungsfreiheit:** Die Fläche darf sich verkleinern — nur um **dokumentierte Drops** (Nicht-Ziel t_74b23096). Hier: die 2 Device-Drops, dokumentiert in Konzept §3.3 + diesem Spike + dem Contract-Test-Update. Die `get_activities`-Signatur-änderung ist eine dokumentierte Breaking-Change (User-Entscheidung), kein Drop.

**Docs-/Repo-Sync-Punkte (in Phase 2 abarbeiten):**

| Ort | Punkt |
|---|---|
| `tests/contract/test_tool_surface.py` | 2 Device-Tools entfernen + `get_activities`-Eintrag auf `(limit, start)` — **Normanker, zuerst aktualisieren** |
| `README.md` §Available Tools | Device-Zeile ("Device tools: device info and connected devices") entfernen |
| `concept.md` | "39 Tools" → "40 Tools" an allen Textstellen (Header §3.3, §1, KISS-Beispiel §5) — Architect-Review hat dies bereits als Nicht-Blocker markiert |
| `.env.template` | `GARMIN_PASSWORD` entfernen (Konzept-Entscheidung; `.env` ist untracked) |
| `login.py` | Header-Kommentar "garth 0.8.0" veraltet (Kosmetik, Phase 3) |

---

## 5. S1-Open-Items (§6) — aufgelöst

| # | Item | S2-Entscheidung |
|---|---|---|
| 1 | Devices: Drop vs. `[]`/`{}`+Warnung | **Drop** (beide Tools, dokumentiert) — konsistent mit User-Regel "leere Tools entfernen". |
| 2 | `get_garmin_scores` Shape-Drift | **Dataclass-Patch** `hill_score: int \| None = 0` (S1-Empfehlung; zentral, kein Tool-Logik-Change). Kein Drop — hohe Nutzwert-Priorität. |
| 3 | `get_activity_map`: Heat-Map vs. Polyline | **Beide Felder** (`activityHeatMapDTO` + `gPolyline`) via `camel_to_snake_dict`, kein Feld-Curating (KISS; der LLM-Client wählt). Name + Payload-Form unverändert. |
| 4 | `get_resting_heart_rate` Granularität | **Tages-Rest-HR** (konsistent mit `day`-Param): `DailyHeartRate.list(end=day, period=1) → [0].resting_heart_rate`; Fallback `DailySummary.get(day)`. Kein 7-Tage-Tool. |
| 5 | `get_sleep_summary` Granularität | **Alias auf `SleepData.get(day)["sleep_summary"]`** (Score-/Dauer-Block). Detail-Phasen bleiben bei `get_sleep_detail` (`DailySleepData`) — klare Trennung Summary vs. Detail. |
| 6 | `get_steps_goal` Endpoint | **Primary:** `/wellness-service/wellness/wellness-goals/consolidated/steps/{day}` (konsolidiert, multi-goal-fähig, n=6); `stats.DailySteps.step_goal`-Feld als Fallback 2. |
| 7 | `get_activities` `limit`/`start` | **User-Entscheidung t_74b23096 schlägt S1-Vorschlag (Wrapper) durch:** Signatur **direkt** auf `get_activities(limit=20, start=0)` — kein Deprecated-Wrapper. Dokumentierte Breaking-Change (legacy `(end, days)` lief nie; Klasse existiert in ng nicht). Contract-Test-Eintrag entsprechend ändern. |

---

## 6. Auswirkung auf Phase 2 (Work-Package-Eingabe)

1. **Erstes WP (Gating):** Contract-Test auf 38 Tools + `get_activities(limit, start)` umstellen — definiert die Ziel-Fläche für alle Folge-WPs.
2. Tool-Migration in Domänen-Batches (S1-Tabelle §1 ist die exakte Zuordnung pro Tool): body/heart/sleep-fixes → steps/stress/hydration → activity/goals → nutrition/PR/blood_pressure (Endpoint-Fallbacks) → devices-Drop.
3. `get_garmin_scores`-Dataclass-Patch als eigenes kleines WP (einzelner Accessor, eigener Test).
4. Docs-Sync-Punkte (§4 Tabelle) als Abschluss-WP (README, Konzept-Textstellen, `.env.template`, `login.py`-Header).
5. Basis für alle WPs: `feature/garth-ng-compat`; Merge auf `main` erst in Phase 7 (PM) mit allen vier Sign-offs.

**Open für User/Architect (keine Blocker):** keine — alle S1-Open-Items sind über User-Entscheidungen + S1-Empfehlungen resolvable und hier festgelegt.