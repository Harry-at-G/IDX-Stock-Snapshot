# IDX Stock Snapshot: starter kit

The starter kit for **Build and Ship a Live IDX Stock App with an AI Pair Programmer**, the GitHub Copilot x Sectors Community Meetup (31 October 2026, Block71 Jakarta).

You build a small web app with GitHub Copilot: an investment calculator that grows into a stock app on live data from the Indonesia Stock Exchange (IDX), using the [Sectors API](https://sectors.app). No coding experience needed. Follow the course site, module by module.

## What's inside

| File | What it is |
|---|---|
| `app.py` | Your app. It starts almost empty; you build it with Copilot |
| `sectors.py` | A ready-made helper that gets IDX data from Sectors. You don't need to change it |
| `requirements.txt` | The Python packages the app needs |
| `.env.example` | A sample secrets file; copy it to `.env` and add your Sectors API key |
| `.gitignore` | Files Git must never save, such as `.env` |
| `.github/copilot-instructions.md` | A short briefing note Copilot reads with every chat |
| `style_reference_1.html` | A sample design to borrow the look from (Module 7.3) |

## Set up (do this before the meetup)

1. Install [VS Code](https://code.visualstudio.com), [Python 3.10 or newer](https://www.python.org/downloads/) (on Windows, tick **Add python.exe to PATH**) and [Git](https://git-scm.com/downloads).
2. In VS Code, install the **GitHub Copilot** and **Python** (by Microsoft) extensions, and sign in with your GitHub account.
3. Get these files, either way:
   - **New to GitHub:** download the ZIP from the course's Google Drive link, unzip it, and open the folder in VS Code (**File → Open Folder**).
   - **Familiar with GitHub:** click **Use this template → Create a new repository**, then clone your copy with **Git: Clone** from the Command Palette.
4. Press `Ctrl+Shift+P` (`Cmd+Shift+P` on a Mac), run **Python: Create Environment**, choose **Venv**, pick your Python, and tick `requirements.txt` so the packages are installed.
5. Open a new terminal (**Terminal → New Terminal**) and run `streamlit run app.py`. A page titled **IDX Stock Snapshot** opens in your browser. Press `Ctrl+C` in the terminal to stop it.

If step 4 fails, make the environment in the terminal instead:

| Step | Windows (PowerShell) | Mac (Terminal) |
|---|---|---|
| Create it | `python -m venv .venv` | `python3 -m venv .venv` |
| Turn it on | `.venv\Scripts\activate` | `source .venv/bin/activate` |
| Install the packages | `pip install -r requirements.txt` | `pip install -r requirements.txt` |

On Windows, if turning it on says running scripts is disabled, run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` once and try again.

## Your Sectors API key

Copy `.env.example` to a new file named `.env` and replace `your-key-here` with your key:

```
SECTORS_API_KEY=your-key-here
```

`.env` stays on your laptop: `.gitignore` keeps it off GitHub. Never put your key in `.env.example`, `app.py` or a Copilot chat. When you deploy to Streamlit Community Cloud, put the key in the app's **Secrets** instead:

```
SECTORS_API_KEY = "your-key-here"
```

## The helper functions

```python
from sectors import get_company_overview, get_daily_prices, get_company_financials, SectorsError

get_company_overview("BBCA")                          # company name, sector, last close, market cap... (1 credit)
get_daily_prices("BBCA", "2026-10-01", "2026-10-27")  # one row per trading day, at most 90 days (1 credit)
get_company_financials("BBCA")                        # yearly financials (1 credit)
```

Every function raises `SectorsError` with a plain message you can show on the page, for example when a ticker doesn't exist or the key is missing.

---

This project shows market data for learning. Nothing in it is investment advice.
