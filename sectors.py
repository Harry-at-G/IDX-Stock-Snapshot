"""
sectors.py: a ready-made helper for getting IDX stock data from the Sectors API.

You do not need to change this file. Your app uses it like this:

    from sectors import get_company_overview, get_daily_prices, SectorsError

    company = get_company_overview("BBCA")
    prices = get_daily_prices("BBCA")

Your API key is read from SECTORS_API_KEY:
  - on your laptop, from the .env file
  - on Streamlit Community Cloud, from the app's Secrets
It never needs to appear in app.py.

API docs: https://docs.sectors.app
"""

import os
from datetime import date, timedelta

import pandas as pd
import requests
from dotenv import load_dotenv

BASE_URL = "https://api.sectors.app/v2"
MAX_DAYS = 90  # Sectors returns at most 90 days of daily prices per request

load_dotenv()  # reads .env on your laptop; does nothing if there is no .env


class SectorsError(Exception):
    """A problem getting data, with a message that is safe to show on the page."""


def _api_key():
    key = os.environ.get("SECTORS_API_KEY")
    if not key:
        # On Streamlit Community Cloud the key lives in Secrets
        try:
            import streamlit as st

            key = st.secrets.get("SECTORS_API_KEY")
        except Exception:
            key = None
    if not key or key == "your-key-here":
        raise SectorsError(
            "No Sectors API key found. Put SECTORS_API_KEY in your .env file "
            "(on your laptop) or in Secrets (on Streamlit Community Cloud)."
        )
    return key


def _clean_ticker(ticker):
    ticker = (ticker or "").strip().upper().replace(".JK", "")
    if not ticker:
        raise SectorsError("Please type a ticker, for example BBCA.")
    return ticker


def _get(path, params=None):
    try:
        response = requests.get(
            f"{BASE_URL}{path}",
            headers={"Authorization": _api_key()},
            params=params,
            timeout=20,
        )
    except requests.RequestException:
        raise SectorsError("Could not reach Sectors. Check your internet connection and try again.")

    if response.status_code in (401, 403):
        raise SectorsError("Sectors did not accept your API key. Check SECTORS_API_KEY.")
    if response.status_code == 400:
        raise SectorsError("That doesn't look like an IDX ticker. Tickers are 4 letters, like BBCA.")
    if response.status_code == 404:
        raise SectorsError("We couldn't find that ticker on IDX.")
    if response.status_code == 429:
        raise SectorsError("Too many requests, or no credits left. Wait a moment and try again.")
    if not response.ok:
        raise SectorsError(f"Sectors returned an error ({response.status_code}). Try again later.")
    return response.json()


def get_company_overview(ticker):
    """
    Basic facts about one IDX company. Costs 1 Sectors credit.

    Gives back one dictionary, for example:
        {
            "symbol": "BBCA.JK",
            "company_name": "PT Bank Central Asia Tbk.",
            "sector": "Financials",
            "sub_sector": "Banks",
            "last_close_price": 4900,          # rupiah per share
            "latest_close_date": "2026-10-27",
            "daily_close_change": -0.0081,     # a fraction: -0.0081 means -0.81%
            "market_cap": 598007267550000,     # rupiah
            "listing_date": "2000-05-31",
            ... and a few more fields
        }
    """
    ticker = _clean_ticker(ticker)
    report = _get(f"/company/report/{ticker}/", params={"sections": "overview"})
    overview = report.get("overview") or {}
    if not report.get("company_name") or not overview:
        raise SectorsError("We couldn't find that ticker on IDX.")
    return {"symbol": report.get("symbol"), "company_name": report.get("company_name"), **overview}


def get_daily_prices(ticker, start=None, end=None):
    """
    Daily prices for one IDX company. Costs 1 Sectors credit.

    start and end are dates (datetime.date or "YYYY-MM-DD"). If you leave them
    out you get the last 30 days. Sectors gives at most 90 days per request:
    for a longer range it returns the most recent 90 days up to end.

    Gives back a table (a pandas DataFrame) with one row per trading day and
    the columns: date, open, high, low, close, volume, market_cap.
    """
    ticker = _clean_ticker(ticker)
    end = pd.to_datetime(end).date() if end else date.today()
    end = min(end, date.today())  # Sectors rejects end dates in the future
    start = pd.to_datetime(start).date() if start else end - timedelta(days=30)
    if start > end:
        raise SectorsError("The start date is after the end date.")

    rows = _get(f"/daily/{ticker}/", params={"start": start.isoformat(), "end": end.isoformat()})
    if not rows:
        raise SectorsError("No prices found for that ticker and dates.")
    prices = pd.DataFrame(rows)
    prices["date"] = pd.to_datetime(prices["date"])
    columns = ["date", "open", "high", "low", "close", "volume", "market_cap"]
    return prices[[c for c in columns if c in prices.columns]].sort_values("date").reset_index(drop=True)


def get_company_financials(ticker):
    """
    Yearly financials for one IDX company (revenue, earnings and more), as
    Sectors returns them in the "financials" section of its company report.
    Costs 1 Sectors credit. Used in the Stretch "financials tab" feature.
    """
    ticker = _clean_ticker(ticker)
    report = _get(f"/company/report/{ticker}/", params={"sections": "financials"})
    financials = report.get("financials")
    if not financials:
        raise SectorsError("No financial data found for that ticker.")
    return financials
