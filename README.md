# Kraken API QA Automation (pytest)

Automated API checks for **Kraken's public REST endpoints** using **Python + pytest**.  
Designed as a portfolio-ready QA project: clear assertions, reusable API client, and CI that runs on every push/PR.

## What this project demonstrates (QA skills)

- **API testing**: schema + data validation (not just status code)
- **Automation**: repeatable test runs locally and in CI
- **Test design**: readable test names, Arrange/Act/Assert structure
- **Reporting**: JUnit output for CI logs/artifacts
- **Tooling**: pytest, requests, GitHub Actions

## Tests included

These tests call Kraken **public** endpoints (no API key needed):

- `/0/public/Time` — server time is returned and looks valid
- `/0/public/Ticker` — price fields exist and parse, values are sane (> 0)
- `/0/public/OHLC` — candle list returned, basic consistency checks
- `/0/public/AssetPairs` — expected pair exists and has required metadata
- `/0/public/Depth` — order book returns bids/asks lists (non-empty)

> Note: Public endpoints can be temporarily slow or rate-limited. The suite is intentionally small and fast.

## Project structure

```
kraken-api-qa-automation/
├─ tests/                 # pytest test suite
├─ utils/                 # KrakenApiClient wrapper (requests)
├─ reports/               # CI artifacts (generated)
├─ requirements.txt       # Python dependencies
└─ .github/workflows/     # CI pipeline (GitHub Actions)
```

## Quick start (local)

### 1) Create & activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```bat
python -m venv .venv
.\.venv\Scripts\activate.bat
```

### 2) Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Run the tests

```bash
pytest -q
```

### (Optional) Generate a JUnit report

```bash
mkdir reports
pytest -q --junitxml=reports/junit.xml
```

## Run / Debug tests in Visual Studio / VS Code

### Visual Studio (Python)
1. Install workload: **Python development**
2. Open the repo folder
3. Make sure your interpreter is the `.venv` you created
4. Open **Test Explorer** → run/debug tests  
   (Tests are not a “startup app”, so F5 is not the default way to run them.)

### VS Code (recommended for Python)
1. Install extension: **Python** (by Microsoft)
2. Select interpreter: `.venv`
3. Testing: enable **pytest**
4. Use “Run Test” / “Debug Test” right in the editor

## CI (GitHub Actions)

The workflow runs on push and pull requests and uploads `reports/` as an artifact.
After you add the workflow file, you can add a badge like this (replace `<USER>`/`<REPO>`):

```md
![CI](https://github.com/<USER>/<REPO>/actions/workflows/ci.yml/badge.svg)
```

## Roadmap (nice upgrades for interviews)

- Add **pytest markers**: `smoke`, `live`, `slow`
- Add **schema validation** (pydantic / jsonschema)
- Add **Allure** or HTML report
- Add **config** via env vars (`BASE_URL`, `SYMBOL`, timeouts)
- Add **negative tests** (invalid pair, missing params, etc.)

## License

MIT
