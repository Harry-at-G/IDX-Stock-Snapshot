# Project briefing for GitHub Copilot

- This is **IDX Stock Snapshot**, a beginner's Streamlit app about stocks on the Indonesia Stock Exchange (IDX).
- The person you are helping has never written code. Explain in plain words, keep answers short, and avoid jargon.
- The app lives in `app.py`. Keep it a single Streamlit file unless asked otherwise.
- Get all market data through the functions in `sectors.py` (`get_company_overview`, `get_daily_prices`, `get_company_financials`). Do not write new API code, do not change `sectors.py`, and do not use any other data provider.
- `sectors.py` raises `SectorsError` with a message that is safe to show. Catch it and show the message with `st.warning`; never show a traceback on the page.
- Never put an API key in code. The key is `SECTORS_API_KEY`, read from `.env` locally and from Streamlit Secrets when deployed.
- Only use packages listed in `requirements.txt`. If a new one is truly needed, add it to `requirements.txt` and say so.
- Money is in rupiah, shown with dots between thousands, like Rp 1.000.000. `daily_close_change` is a fraction (-0.0081 means -0.81%). `market_cap` is in rupiah. One lot is 100 shares.
- The app shows data, not advice: keep a short line on the page saying it is not investment advice.
