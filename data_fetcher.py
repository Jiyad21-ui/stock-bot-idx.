"""
data_fetcher.py — Ambil data OHLCV dari Yahoo Finance untuk saham IDX (.JK)
"""

import logging
import time
import yfinance as yf
import pandas as pd
from typing import Optional
from config import INDICATORS

logger = logging.getLogger(__name__)


def fetch_ohlcv(ticker: str, period: str = None, retries: int = 3) -> Optional[pd.DataFrame]:
    """
    Ambil data OHLCV dari Yahoo Finance.
    Return DataFrame dengan kolom: Open, High, Low, Close, Volume
    Return None jika gagal.
    """
    period = period or INDICATORS["data_period"]

    for attempt in range(retries):
        try:
            df = yf.download(
                ticker,
                period=period,
                interval="1d",
                progress=False,
                auto_adjust=True,
                threads=False,
            )

            if df is None or df.empty:
                logger.warning(f"[{ticker}] Data kosong dari Yahoo Finance")
                return None

            # Flatten MultiIndex columns jika ada
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # Pastikan kolom yang dibutuhkan ada
            required = {"Open", "High", "Low", "Close", "Volume"}
            if not required.issubset(df.columns):
                logger.warning(f"[{ticker}] Kolom tidak lengkap: {df.columns.tolist()}")
                return None

            # Hapus baris dengan NaN di kolom kritis
            df = df.dropna(subset=["Close", "Volume"])

            # Minimal butuh 200 hari data untuk EMA-200
            if len(df) < 60:
                logger.warning(f"[{ticker}] Data terlalu sedikit: {len(df)} baris")
                return None

            df.index = pd.to_datetime(df.index)
            df = df.sort_index()

            logger.info(f"[{ticker}] Berhasil fetch {len(df)} baris data (s/d {df.index[-1].date()})")
            return df

        except Exception as e:
            logger.error(f"[{ticker}] Error attempt {attempt+1}/{retries}: {e}")
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))  # exponential backoff

    return None


def fetch_batch(tickers: list, delay: float = 0.5) -> dict:
    """
    Fetch data untuk banyak ticker sekaligus.
    Return dict {ticker: DataFrame atau None}
    """
    results = {}
    total = len(tickers)

    for i, ticker in enumerate(tickers, 1):
        logger.info(f"Fetching [{i}/{total}] {ticker}...")
        results[ticker] = fetch_ohlcv(ticker)
        if delay > 0:
            time.sleep(delay)  # Hindari rate limit Yahoo

    success = sum(1 for v in results.values() if v is not None)
    logger.info(f"Fetch selesai: {success}/{total} ticker berhasil")
    return results


def get_latest_price(ticker: str) -> Optional[dict]:
    """Ambil harga terakhir beserta info ringkas."""
    df = fetch_ohlcv(ticker, period="5d")
    if df is None or df.empty:
        return None

    last  = df.iloc[-1]
    prev  = df.iloc[-2] if len(df) >= 2 else last

    change    = last["Close"] - prev["Close"]
    change_pct = (change / prev["Close"]) * 100

    return {
        "ticker":      ticker,
        "close":       round(float(last["Close"]), 2),
        "open":        round(float(last["Open"]), 2),
        "high":        round(float(last["High"]), 2),
        "low":         round(float(last["Low"]), 2),
        "volume":      int(last["Volume"]),
        "change":      round(float(change), 2),
        "change_pct":  round(float(change_pct), 2),
        "date":        str(df.index[-1].date()),
    }
