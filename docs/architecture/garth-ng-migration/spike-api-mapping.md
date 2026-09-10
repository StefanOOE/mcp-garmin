# Spike S1 — Live API-Mapping: garth 0.x → garth-ng 1.1.0

**Spike-Card:** S1 = `t_7756ff1b` (API-Mapping)
**Auflösung von:** U1 (`concept.md` §4) — exakter Accessor/Endpoint pro Tool inkl. Live-Payload-Shape für alle 40 Tools; welche "drop-Kandidaten" (§3.3) live Daten liefern.
**Datum:** 2026-09-10 (Run #49, frischer Token) · **konsolidiert + Spot-Check Run #51 am 2026-09-11 00:15 CEST** (frischer Token, 19 h Restgültigkeit — alle 8 Endpoint-Fallbacks, `resting_heart_rate`-Komposition, `HRVData.list`, Sleep neu live bestätigt)
**Basis-Repo:** `/home/ss/src/mcp-garmin`, Branch `feature/garth-ng-compat`
**Live-Umfeld:** `garth 1.1.0` (`.venv/lib/python3.12/site-packages/garth`), Token via `GARTH_HOME=~/.garth` (auto-resumed + `refresh_token()`), Profil mit echten Daten (Activities, Sleep, Steps, Weight, BloodPressure, BodyBattery, HRV, Training, PRs, Goals, Nutrition).

> **Sprache:** Deutsch (wie `concept.md`); Status-Labels englisch (wie in `concept.md` §3.3).

---

## 0. Executive Summary

Von 40 Tools: **31 liefern live Daten** (11 × 1:1 + 18 × Remap), **8 sind live verifiziert per Endpoint-Fallback** (`client.connectapi`), **2 sind Drop-Kandidaten** (`get_device_info`, `get_connected_devices`), **1 hat ein Live-Payload-Shape-Drift** (`get_garmin_scores` — Dataclass-Validierung). **Kein Tool ist ein harter „Endpoint 404 + kein Accessor" ohne Fallback** — die Device-Domain ist die einzige echte Lücke.

**Wichtigste Korrektur zu `concept.md` §3.3:** `connectapi(path)` baut `https://connectapi.garmin.com{path}` (siehe `http.py:168` + `connectapi()` in `http.py:275-281`). Pfade werden daher **ohne** `/connectapi`- oder `/proxy`-Präfix übergeben. Die in §3.3 vermuteten Pfade (`/personalservice-service/prs`, `/nutrition-log-service/log/nutrition/{date}` u. a.) sind **falsch** — die tatsächlich liefernden Pfade sind unten live verifiziert.

### Status-Legende
| Label | Bedeutung |
|---|---|
| `1:1` | Accessor vorhanden, Methodensignatur + Semantik unverändert (nur Import-Pfad) |
| `Remap` | Accessor vorhanden, aber Klasse/Signatur/Namespace geändert — Code-Änderung nötig |
| `Endpoint-Fallback` | Kein ng-Accessor → `client.connectapi("/<service>/<path>")` + `camel_to_snake_dict()` im Tool (live-verifizierter Pfad) |
| `Drop-Kandidat` | Kein Accessor **und** kein live liefernder Endpoint → S2 entscheidet: entfernen oder `[]`/`{}`+Warnung |
| `Shape-Drift` | Accessor liefert, aber Dataclass-Validierung bricht an Live-Payload — Dataclass-/Tool-Änderung nötig |
| `bereits migriert` | compat-Branch nutzt den ng-Accessor bereits (kein S1-Aktion) |

### URL-Kontrakt (entscheidend für alle Endpoint-Fallbacks)
```python
client.connectapi("/activity-service/activity/{id}/mapdetails")
# → GET https://connectapi.garmin.com/activity-service/activity/{id}/mapdetails
#   OAuth2-Token aus GARTH_HOME, api=True
```
- `connectapi(path, method="GET", params=..., json=...)` → `request(method, "connectapi", path, api=True)`.
- **Kein** `/connectapi`/`/proxy`-Präfix im `path`-Argument.
- 204 → `None`. sonst → `resp.json()`.
- Fehler: `garth.exc.GarthHTTPError` (HTTP-Status) bzw. `garth.exc.GarthException` (Token o. ä.) — `errors.py` maps das bereits.

---

## 1. Live-Verifikation — Vollständige Tabelle (40 Tools)

Spalten: **Tool** (Name bleibt, außer "→") · **Legacy (main)** (Klasse · Methode, `import_mod.data`) · **garth-ng-Ziel** (Accessor + exakte Signatur/Pfad) · **Status** · **Live** (Run #49 Ergebnis: Felder/Units).

### 1.1 Activity

| Tool | Legacy (main) | garth-ng-Ziel | Status | Live (Run #49) |
|---|---|---|---|---|
| `get_activities` | `Activities.list(end, days)` | `garth.data.Activity.list(limit: int=20, start: int=0, *, client)` | **Remap** (Signatur!) | OK n=5. **Breaking:** kein `end`/`days` mehr — `limit`+`start` (Pagination). Tool-Rechner: `limit=days`, `start` aus Offset. |
| `get_activity_detail` | `ActivityDetail.get(activity_id)` | `garth.data.Activity.get(activity_id=..., *, client)` | **Remap** (Klassenname) | OK n=1. Payload: `activity_id, activity_name, activity_type, start_date, distance_meters, duration_seconds, calories, avg_heart_rate, max_heart_rate, ...` |
| `get_activity_map` | `ActivityMap.get(activity_id)` | **kein Accessor** (`Activity.map_details` **nicht** in 1.1.0, `hasattr` False) → `client.connectapi(f"/activity-service/activity/{activity_id}/mapdetails")` | **Endpoint-Fallback** | OK. Payload-Keys: `activityHeatMapDTO`, `gPolyline` (camelCase → `camel_to_snake_dict`). **Korrektur §3.3:** `/map` war falsch, korrekt ist `/mapdetails`. |
| `get_fitness_activities` | `FitnessActivities.list(end, days)` | `garth.data.FitnessActivity.list(end: str, days: int, *, client)` | **Remap** (Klassenname) | OK n=0 (adaptive coaching, Konto leer — Endpunkt liefert). |
| `get_personal_records` | `PersonalRecords.get()` | **kein Accessor** → `client.connectapi("/personalrecord-service/personalrecord")` | **Endpoint-Fallback** | OK n=16. **Korrektur §3.3:** `/personalservice-service/prs` falsch. Payload: PR-Liste (camelCase). |
| `get_personal_record_types` | `PersonalRecordTypes.get()` | **kein Accessor** → `client.connectapi("/personalrecord-service/personalrecordtype")` | **Endpoint-Fallback** | OK n=51. **Korrektur §3.3:** `/personalservice-service/prs/types` falsch. |

> Optional (kein Tool, nur Referenz): `client.connectapi(f"/personalrecord-service/personalrecord/prByActivityId/{activity_id}")` → PRs pro Activity (Run #49 n=0, Endpunkt live).

### 1.2 Body

| Tool | Legacy (main) | garth-ng-Ziel | Status | Live (Run #49) |
|---|---|---|---|---|
| `get_body_weight` | `WeightData.get(day)` | `garth.data.WeightData.get(day=..., *, client)` | **1:1** | OK n=1. **Gewicht in Gramm** (`weight: 95010.0` g ≈ 95 kg) + `bmi`, `body_fat_percent` — Units unverändert gegenüber main (Contract). |
| `get_weight_history` | `WeightData.list(end, days)` | `garth.data.WeightData.list(end=..., days=..., *, client)` | **1:1** | OK n=1. `dateWeightList[]` (pro Tag `weight` g, `bmi`, `bodyFat`). Leerer Tag → leere Liste (kein 404). |
| `get_blood_pressure` | `BloodPressure.get(day)` | **kein Accessor** → `client.connectapi(f"/bloodpressure-service/bloodpressure/dayview/{day}")` | **Endpoint-Fallback** | OK n=5. **Korrektur §3.3:** `/usersummary-service/usersummary/bloodpressure` falsch. Payload: Lese-Werte (systolisch/diastolisch/puls) camelCase. |
| `get_body_battery` | `BodyBatteryData.get(day)` | `garth.data.body_battery.BodyBatteryData.get(day=..., *, client)` | **1:1** | OK n=1. Readings-Liste (`body_battery_value`, Zeitstempel). |
| `get_body_battery_stress` | `DailyBodyBatteryStress.get(day)` | `garth.data.body_battery.DailyBodyBatteryStress.get(day=..., *, client)` | **1:1** | OK n=1. |
| `get_body_battery_stress_history` | `DailyBodyBatteryStress.list(end, days)` | `garth.data.body_battery.DailyBodyBatteryStress.list(end=..., days=..., *, client)` | **1:1** | OK n=2. |

### 1.3 Devices

| Tool | Legacy (main) | garth-ng-Ziel | Status | Live (Run #49) |
|---|---|---|---|---|
| `get_connected_devices` | `ConnectedDevices.get()` | **kein Accessor**; `garth/data/deviceinfo.py` **leere Datei (0 Bytes)**, Klasse nicht in `__all__`. Raw-Candidate `/deviceinfo-service/devices` → **404** (alle Präfix-Varianten: `/deviceinfo-service/devices`, `/proxy/deviceinfo-service/devices`, `/userdevices-service/device`). | **Drop-Kandidat** | **404** (alle Varianten). S2: entfernen oder `[]`+Warnung. |
| `get_device_info` | `DeviceInfo.get(device_id)` | wie oben — kein Accessor, kein live Endpoint. **Signature-Änderung nötig falls behalten:** ng-Endpoint hat keinen `device_id`-Parameter → `get_device_info()` ohne Param. | **Drop-Kandidat** | **404**. S2 entscheidet. |

> **Einzige echte Lücke der gesamten Migration.** Keine ng-1.1.0-Accessor und kein verifizierbarer connectapi-Endpunkt für Device-Domain. Empfehlung: beide Tools als Drop behandeln (leere Device-Liste verwirrt den LLM-Client mehr, als sie hilft).

### 1.4 Goals

| Tool | Legacy (main) | garth-ng-Ziel | Status | Live (Run #49) |
|---|---|---|---|---|
| `get_steps_goal` | `StepsGoal.get()` | **kein Accessor** → `client.connectapi(f"/wellness-service/wellness/wellness-goals/consolidated/steps/{day}")` | **Endpoint-Fallback** | OK n=6. **Korrektur §3.3:** `DailySteps.step_goal`-Feld-Ersatz nicht nötig — eigener Endpoint liefert konsolidierte Goals. **Alternativ (Fallback 2):** `stats.DailySteps.list` enthält `step_goal` pro Tag. |
| `get_weight_goal` | `WeightGoal.get()` | **kein Accessor** → `client.connectapi(f"/goal-service/goal/user/effective/weightgoal/{day}/{day}")` | **Endpoint-Fallback** | OK n=2. **Korrektur §3.3:** `/usersummary-service/usersummary/weight/goal` falsch. |
| `get_garmin_scores` | `GarminScores.get()` | `garth.data.GarminScoresData.get(day=..., *, client)` → 2 Requests: `/metrics-service/metrics/hillscore` + `/metrics-service/metrics/endurancescore` | **Shape-Drift** | **FAIL (Dataclass).** `GarminScoresData` (pydantic) verlangt `hill_score: int`, `hill_endurance_score: int` — Live liefert `None` (Konto ohne Hill/Endurance-Daten) → `3 validation errors (int_type, input_value=None)`. **Fix-Optionen:** (a) `errors.py`/Tool: `None→0` vor Validierung; (b) Dataclass-Patch `hill_score: int | None = 0`; (c) Tool liefert `{"hill_score": None, "endurance_score": None}` + Warnung. |

### 1.5 Heart

| Tool | Legacy (main) | garth-ng-Ziel | Status | Live (Run #49) |
|---|---|---|---|---|
| `get_daily_heart_rate` | `HeartRateData.get(day)` | `garth.data.DailyHeartRate.get(day=..., *, client)` | **Remap** (Klassenname) | OK n=1. Readings (`hour_heart_rates[]` mit `min_heart_rate`, `max_heart_rate`, `avg_heart_rate`). |
| `get_hrv` | `HrvData.get(day)` | `garth.data.HRVData.list(end=..., days=..., *, client)` | **Remap** (Klasse + `.get`→`.list`) | OK n=3. `day_hrv_data[]` (`avg_hrv`, `min_hrv`, `max_hrv`). **Kein** `.get` — nur `.list`. |
| `get_resting_heart_rate` | `RestingHeartRateData.get(day)` | **kein dedizierter Accessor**. Resting-HR ist **Feld in** `garth.data.DailyHeartRate` (`resting_heart_rate` pro Tag via `.list`) **und** in `garth.data.DailySummary.resting_heart_rate`. | **Remap** (Komposition) | OK. Empfehlung: `DailyHeartRate.list(end=day, days=1)` → `[0].resting_heart_rate` (oder `DailySummary.get(day).resting_heart_rate`). |

### 1.6 Hydration

| Tool | Legacy (main) | garth-ng-Ziel | Status | Live (Run #49) |
|---|---|---|---|---|
| `get_daily_hydration` | `HydrationData.get(day)` | **kein `data.*`-Accessor** → `garth.stats.DailyHydration.list(end=..., period: int, *, client)` (per-Tag Eintrag extrahieren) | **Remap** (Namespace `data`→`stats`, `.get`→`.list`) | OK (n=0 am Tag, Endpunkt liefert). **Korrektur:** kein `data/HydrationData` mehr; nur `stats.DailyHydration`. |
| `get_hydration_history` | `HydrationData.list(end, days)` | `garth.stats.DailyHydration.list(end=..., period: int, *, client)` (`period=days`) | **Remap** (Namespace + `days`→`period`) | OK n=0. |

### 1.7 Nutrition

| Tool | Legacy (main) | garth-ng-Ziel | Status | Live (Run #49) |
|---|---|---|---|---|
| `get_nutrition_log` | `NutritionLog.get(day)` | **kein Accessor** → `client.connectapi(f"/nutrition-service/food/logs/{day}")` | **Endpoint-Fallback** | OK n=7. **Korrektur §3.3:** `/nutrition-log-service/log/nutrition/{date}` falsch. Payload: Mahlzeiten (camelCase). |
| `get_nutrition_status` | `NutritionStatus.get(day)` | **kein Accessor** → `client.connectapi("/nutrition-service/user/nutritionCurrentStatus")` (kein `day`-Param — aktueller Status) | **Endpoint-Fallback** | OK n=3. **Korrektur §3.3:** `/nutrition-status-service/status` falsch. |

### 1.8 Sleep

| Tool | Legacy (main) | garth-ng-Ziel | Status | Live (Run #49) |
|---|---|---|---|---|
| `get_sleep` | `SleepData.get(day)` | `garth.data.SleepData.get(day=..., *, client)` | **1:1** (bereits migriert) | OK n=1. `sleep_summary` (Dauer, Phasen). |
| `get_sleep_detail` | `SleepDetailData.get(day)` | `garth.data.DailySleepData.get(day=..., *, client)` | **1:1** (bereits migriert; Klasse hieß `SleepDetailData`→`DailySleepData`) | OK n=1. Detail-Phasen. |
| `get_sleep_summary` | `SleepSummaryData.get(day)` | **kein separater Accessor** — `SleepData.get(day)` enthält bereits `sleep_summary`-Block. | **Remap** (Zusammenführung) | OK. `SleepData.get` liefert Summary + Detail; `get_sleep_summary` wird Alias auf `SleepData.get(...)["sleep_summary"]` (oder `DailySleepData.get` je nach gewünschtem Granularitäts-Level). S2 bestätigt Granularität. |

### 1.9 Steps / Summary

| Tool | Legacy (main) | garth-ng-Ziel | Status | Live (Run #49) |
|---|---|---|---|---|
| `get_daily_steps` | `StepsData.get(day)` | **kein `data.*`-Accessor** → `garth.stats.DailySteps.list(end=day, period=1, *, client)` → `[0]` | **Remap** (Namespace + `.get`→`.list`) | OK n=1. `steps`, `step_goal` (Fallback für `get_steps_goal`), `distance_meters`, `calories_burned`. |
| `get_weekly_steps` | `WeeklyStepsData.get(start_date)` | `garth.stats.WeeklySteps.list(end=..., period: int, *, client)` | **Remap** (Klasse + `start_date`→`end`) | OK n=1. Wochen-Steps. |
| `get_daily_summary` | `DailySummary.get(day)` | `garth.data.DailySummary.get(day=..., *, client)` | **1:1** | OK n=1. 40+ Felder (Steps, Kalorien, HR, Stress, Sleep, SpO2, Respiration). |
| `get_daily_summary_history` | `DailySummary.list(end, days)` | `garth.data.DailySummary.list(end=..., days=..., *, client)` | **1:1** | OK n=2. |

### 1.10 Stress / Training

| Tool | Legacy (main) | garth-ng-Ziel | Status | Live (Run #49) |
|---|---|---|---|---|
| `get_daily_stress` | `DailyStressData.get(day)` | **kein `data.*`-Accessor** → `garth.stats.DailyStress.list(end=day, period=1, *, client)` → `[0]` | **Remap** (Namespace + `.get`→`.list`) | OK n=1. `stress` (avg/max/min pro Tag). |
| `get_weekly_stress` | `WeeklyStressData.get(start_date)` | `garth.stats.WeeklyStress.list(end=..., period: int, *, client)` | **Remap** (Klasse + Param) | OK n=1. |
| `get_training_status_daily` | `TrainingStatusDaily.get(day)` | `garth.stats.training_status.DailyTrainingStatus.list(end=day, period=1, *, client)` → `[0]` | **Remap** (Namespace + `.get`→`.list`) | OK n=1. `training_status` (score, produktivität, erholung, körperlicher Zustand). |
| `get_training_status_weekly` | `TrainingStatusWeekly.get(start_date)` | `garth.stats.training_status.WeeklyTrainingStatus.list(end=..., period: int, *, client)` | **Remap** | OK n=1. |
| `get_training_status_monthly` | `TrainingStatusMonthly.get(start_date)` | `garth.stats.training_status.MonthlyTrainingStatus.list(end=..., period: int, *, client)` | **Remap** | OK n=1. |
| `get_training_readiness` | `TrainingReadiness.get(day)` | `garth.data.TrainingReadinessData.get(day=..., *, client)` | **Remap** (Klassenname) | OK n=2. Readiness-Score + Komponenten. |
| `get_morning_readiness` | `MorningReadiness.get(day)` | `garth.data.MorningTrainingReadinessData.get(day=..., *, client)` | **Remap** (Klassenname) | OK n=1. |

### 1.11 Util

| Tool | Legacy (main) | garth-ng-Ziel | Status | Live (Run #49) |
|---|---|---|---|---|
| `get_user_profile` | `UserProfile.get()` (`data`) | `garth.users.UserProfile.get(*, client)` — **top-level** `garth.UserProfile` verfügbar; Modulpfad `garth.users.profile` | **1:1** (Import-Pfad) | OK n=1. `profile_id`, `display_name`, `full_name`, `user_name`, `primary_activity`, `location`, ... (64 Felder). |
| `get_user_settings` | `UserSettings.get()` (`data`) | `garth.users.UserSettings.get(*, client)` — top-level; Modulpfad `garth.users.settings` | **1:1** (Import-Pfad) | OK n=1. `units`, `weights` (g/kg), `start_of_week`, `default_locale`, `country`, `default_activity_goal`, ... |

> **Auth (nicht-Tool, Kontext):** `garth.http.client` (Singleton) + `client.refresh_token()` (Methode, persistiert nach `GARTH_HOME`) + `client.user_profile`. `login.py` nutzt `client.login(email, password, prompt_mfa=...)`. `GarthException`-Mapping in `errors.py` unverändert.

---

## 2. Aggregierte Status-Übersicht (40 Tools)

| Status | Anzahl | Tools |
|---|---|---|
| **1:1** (Accessor, Signatur + Semantik stabil) | **11** | `get_body_weight`, `get_weight_history`, `get_body_battery`, `get_body_battery_stress`, `get_body_battery_stress_history`, `get_sleep`, `get_sleep_detail`, `get_daily_summary`, `get_daily_summary_history`, `get_user_profile`, `get_user_settings` |
| **Remap** (Accessor vorhanden, aber Klassenname/Namespace/Signatur geändert) | **18** | `get_activities` (limit/start), `get_activity_detail` (Klasse), `get_fitness_activities` (Klasse), `get_daily_heart_rate` (Klasse), `get_hrv` (Klasse + .get→.list), `get_resting_heart_rate` (Komposition), `get_daily_hydration` (data→stats, .get→.list), `get_hydration_history` (data→stats, days→period), `get_sleep_summary` (Zusammenführung in `SleepData`), `get_daily_steps` (data→stats, .get→.list), `get_weekly_steps` (Klasse + Param), `get_daily_stress` (data→stats, .get→.list), `get_weekly_stress` (Klasse + Param), `get_training_status_daily` (data→stats), `get_training_status_weekly` (data→stats), `get_training_status_monthly` (data→stats), `get_training_readiness` (Klasse), `get_morning_readiness` (Klasse) |
| **Endpoint-Fallback** (`client.connectapi`, kein Accessor) | **8** | `get_activity_map`, `get_personal_records`, `get_personal_record_types`, `get_blood_pressure`, `get_steps_goal`, `get_weight_goal`, `get_nutrition_log`, `get_nutrition_status` |
| **Shape-Drift** (Accessor liefert, Dataclass-Validierung bricht an Live-Payload) | **1** | `get_garmin_scores` (`hill_score`/`hill_endurance_score` `None` → `int` erwartet) |
| **Drop-Kandidat** (kein Accessor, kein live Endpoint) | **2** | `get_connected_devices`, `get_device_info` |

**Summe: 40 Tools** = 11 (1:1) + 18 (Remap) + 8 (Endpoint-Fallback) + 1 (Shape-Drift) + 2 (Drop-Kandidat). Jeder der 40 Tools hat genau einen Primär-Status; die Remap-Zeile zählt 18 Einzeltools (Details oben §1).

---

## 3. Endpoint-Fallback — exakte live-verifizierte Pfade (für `tools/*`-Umsetzung)

Alle Pfade **ohne** `/connectapi`- oder `/proxy`-Präfix (URL-Kontrakt §0). Alle liefen in Run #49 mit echten Daten:

| Tool | `client.connectapi(...)` Pfad | Live n | Payload (Top-Keys, camelCase) |
|---|---|---|---|
| `get_activity_map` | `f"/activity-service/activity/{activity_id}/mapdetails"` | OK | `activityHeatMapDTO`, `gPolyline` |
| `get_personal_records` | `"/personalrecord-service/personalrecord"` | 16 | PR-Liste |
| `get_personal_record_types` | `"/personalrecord-service/personalrecordtype"` | 51 | PR-Type-Liste |
| `get_blood_pressure` | `f"/bloodpressure-service/bloodpressure/dayview/{day}"` | 5 | systolisch/diastolisch/puls |
| `get_steps_goal` | `f"/wellness-service/wellness/wellness-goals/consolidated/steps/{day}"` | 6 | konsolidierte Goals |
| `get_weight_goal` | `f"/goal-service/goal/user/effective/weightgoal/{day}/{day}"` | 2 | weight-goal-Objekt |
| `get_nutrition_log` | `f"/nutrition-service/food/logs/{day}"` | 7 | Mahlzeiten |
| `get_nutrition_status` | `"/nutrition-service/user/nutritionCurrentStatus"` | 3 | aktueller Status (kein `day`) |

> **Optional (kein Tool):** `f"/personalrecord-service/personalrecord/prByActivityId/{activity_id}"` (PRs pro Activity, Run #49 n=0, Endpunkt live).

**Umsetzungsmuster** (in `tools/*.py`, nach `concept.md` §3.2):
```python
raw = client.connectapi(f"/personalrecord-service/personalrecord")
return [camel_to_snake_dict(x) for x in raw]
```

---

## 4. Korrekturen zu `concept.md` §3.3 (Vorphauswertung → Live-Befund)

| §3.3-Vermutung | Live-Befund (Run #49) |
|---|---|
| Personal-Records Endpoints `/personalservice-service/prs`, `/prs/types` | **Falsch.** `/personalrecord-service/personalrecord`, `/personalrecord-service/personalrecordtype` (n=16/51). |
| BloodPressure `/usersummary-service/usersummary/bloodpressure` | **Falsch.** `/bloodpressure-service/bloodpressure/dayview/{day}` (n=5). |
| Nutrition `/connectapi/proxy/nutrition-log-service/log/nutrition/{date}`, `/nutrition-status-service/status` | **Falsch.** `/nutrition-service/food/logs/{day}` (n=7), `/nutrition-service/user/nutritionCurrentStatus` (n=3). |
| Weight goal `/usersummary-service/usersummary/weight/goal` | **Falsch.** `/goal-service/goal/user/effective/weightgoal/{day}/{day}` (n=2). |
| Activity Map `Activity.map_details` falls in 1.1.0 vorhanden | **Nicht vorhanden** (keine Methode). Fallback `/activity-service/activity/{id}/mapdetails` (n=OK). `/map` aus §3.3 war falsch. |
| Steps goal „`DailySteps.step_goal`-Feld ersetzt" | **Nicht nötig.** `/wellness-service/wellness/wellness-goals/consolidated/steps/{day}` liefert konsolidiert (n=6). `step_goal`-Feld als Fallback 2 vorhanden. |
| Devices `/proxy/deviceinfo-service/device[s]` | **404** in allen Varianten. `deviceinfo.py` ist **leere Datei (0 Bytes)**. → Drop. |
| Sleep „bereits migriert" (`SleepData`/`DailySleepData`) | **Bestätigt** — beide Accessor live (n=1). `SleepSummaryData` als separater Accessor nicht vorhanden (Summary in `SleepData`). |
| `get_garmin_scores` „1:1" | **Shape-Drift.** `GarminScoresData` (pydantic) bricht an `hill_score=None` (int erwartet). Dataclass-/Tool-Fix nötig. |

---

## 5. Units & Contract (unverändert gegenüber main)

- **Gewicht in Gramm** — `WeightData.get/list` liefert `weight: 95010.0` (g). Tool-Contract unverändert.
- **Timestamps** ISO 8601 — unverändert.
- **camelCase → snake_case** — `serialization.py` (`camel_to_snake_dict`) bleibt; wird von allen Endpoint-Fallbacks + Accessor-Payloads genutzt.
- **Feldnamen** — Accessor-Payloads folgen dem bestehenden camelCase-Format; `project_sleep_fields` (Sleep) unverändert.
- **Profil-Einheiten** — `UserSettings` liefert `units`/`weights` (g/kg, metrisch) — kein Unit-Mapping im Tool nötig.

---

## 6. Open Items für S2 (Scope/Strategy)

1. **`get_connected_devices` / `get_device_info`**: Drop (Empfehlung) vs. `[]`/`{}`+Warnung. Ng hat keine Device-Domain (leere `deviceinfo.py`). Falls behalten: `get_device_info()` ohne `device_id`-Param (ng-Endpoint parametrisiert nicht pro Device).
2. **`get_garmin_scores` Shape-Drift**: Fix-Strategie (Dataclass-Patch `int|None=0` vs. Tool-`None→0` vs. `0`-Default). Empfehlung: Dataclass-Patch `hill_score: int | None = 0` (zentral, betrifft nur diesen Accessor; kein Tool-Logik-Änderung).
3. **`get_activity_map`**: Name bleibt. Payload `activityHeatMapDTO`+`gPolyline` → `camel_to_snake_dict`. S2 bestätigt, ob Heat-Map oder nur Polyline an den LLM-Client geht.
4. **`get_resting_heart_rate`**: Komposition aus `DailyHeartRate.list`/`DailySummary.get` (kein dedizierter Accessor). S2 bestätigt Granularität (Tages-Rest-HR vs. 7-Tage-Durchschnitt).
5. **`get_sleep_summary`**: Alias auf `SleepData.get(...)["sleep_summary"]` oder `DailySleepData.get` — S2 bestätigt Granularitäts-Level (Summary vs. Detail-Phasen).
6. **`get_steps_goal`**: Primary-Endpoint `/wellness-service/wellness/wellness-goals/consolidated/steps/{day}` vs. Fallback `stats.DailySteps.step_goal`-Feld. Empfehlung: Primary (konsolidiert, multi-Goal-fähig).
7. **`Activity.list` Breaking-Change** (`limit`/`start` statt `end`/`days`): Tool-Wrapper rechnet `days→limit`. S2 bestätigt, dass Tool-Signatur `get_activities(end, days)` für den LLM-Client stabil bleibt (Wrapper kapselt).

---

## 7. Referenz — Live-Probe-Artefakte (Workspace `probe/`)

| Datei | Inhalt |
|---|---|
| `live_results.json` | Run #49 Voll-Probe (43 Checks, 2026-09-10, frischer Token) — **Primärquelle** für diese Tabelle |
| `live_probe.py` | Das Probe-Skript (klassenbasiert + raw `connectapi`) |
| `ng_surface_full.txt/.json` | garth-ng 1.1.0 Full-Surface (alle `def` + Endpoints) |
| `legacy_map.txt`, `legacy_methods.txt`, `legacy_paths.txt` | Legacy 0.x Surface (Klassen/Methoden/Pfade) |
| `final_stats2.json`, `final_data.json`, `final_spotcheck.json`, `confirm_raw.json`, `device_final.py` | Folge-Proben: `garth.stats.*` Remaps, Device-Endpunkte, GarminScores-Raw-Payload |
| `tool_map.json` | 40-Tool-Inventar (Legacy-Klassen + Methoden + Params) — „from"Seite dieser Tabelle |

**Reproduzierbarkeit:**
```bash
GARTH_HOME=~/.garth /home/ss/src/mcp-garmin/.venv/bin/python \
  /home/ss/.hermes/kanban/boards/mcp-garmin/workspaces/t_7756ff1b/probe/live_probe.py
```
(Token wird via `GARTH_HOME` auto-resumed; `client.refresh_token()` am Anfang. Kein SSO nötig für diesen Run.)

---

## 8. DoD-Erfüllung (S1)

- [x] Exakter Accessor/Endpoint pro Tool für alle 40 Tools (Tabelle §1)
- [x] Live-Payload-Shape (Feldnamen, Units) verifiziert (Run #49, frischer Token, 2026-09-10)
- [x] Run #51 Spot-Check (2026-09-11): alle 8 Endpoint-Fallbacks liefern 200 mit korrekten camelCase-Keys; `resting_heart_rate` (45) + `last_seven_days_avg_resting_heart_rate` (48) live in `DailyHeartRate.list` **und** `DailySummary.get` → Kompositions-Mapping §1.5 bestätigt; `HRVData.list` n=2, `DailySleepData.get` mit Phasen-Feldern, GarminScores Shape-Drift reproduzierbar (Dataclass `int` vs. Live-`None`). Probe-Skripte: `probe/spotcheck51.py`, `probe/spotcheck51b.py`.
- [x] Welche „drop-Kandidaten" (§3.3) live Daten liefern → 8 von 11 liefern (alle Devices + GarminScores-Shape sind die Ausnahme)
- [x] Exakte `connectapi`-Pfade live verifiziert (Tabelle §3)
- [x] Korrekturen zu §3.3-Vorphauswertung dokumentiert (Tabelle §4)
- [x] Units/Contract unverändert bestätigt (§5)
- [x] Open Items für S2 klar abgegrenzt (§6)

**S1 ist abgeschlossen.** S2 (`t_d1a88188`, `spike-scope.md`) kann auf dieser Tabelle aufbauen.