"""
technical_analysis.py — Hitung semua indikator teknikal untuk saham IDX
Menggunakan pandas-ta untuk kalkulasi yang akurat dan cepat
"""

import logging
import numpy as np
import pandas as pd
import pandas_ta as ta
from typing import Optional
from config import INDICATORS

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────────────────────────────────────

def _safe_val(series, idx=-1, decimals=4):
    """Ambil nilai dari series dengan aman, return None jika NaN."""
    try:
        val = series.iloc[idx]
        if pd.isna(val):
            return None
        return round(float(val), decimals)
    except Exception:
        return None


def _pct(a, b, decimals=2):
    """Hitung persentase selisih: (a - b) / b * 100"""
    if b and b != 0:
        return round((a - b) / abs(b) * 100, decimals)
    return 0.0


# ─────────────────────────────────────────────────────────────────────────────
# SUPPORT & RESISTANCE DETECTION
# ─────────────────────────────────────────────────────────────────────────────

def detect_support_resistance(df: pd.DataFrame, lookback: int = None) -> dict:
    """
    Deteksi level Support & Resistance menggunakan pivot points
    dan clustering harga pada high/low historis.
    """
    lookback = lookback or INDICATORS["sr_lookback"]
    recent   = df.tail(lookback)
    close    = float(df["Close"].iloc[-1])

    highs = recent["High"].values
    lows  = recent["Low"].values

    # Pivot high & low dengan window 5
    pivot_highs, pivot_lows = [], []
    for i in range(2, len(recent) - 2):
        if highs[i] == max(highs[i-2:i+3]):
            pivot_highs.append(highs[i])
        if lows[i] == min(lows[i-2:i+3]):
            pivot_lows.append(lows[i])

    # Clustering: gabungkan level yang berdekatan (dalam 1%)
    def cluster(levels, tol=0.01):
        if not levels:
            return []
        levels = sorted(levels)
        clusters = [[levels[0]]]
        for lv in levels[1:]:
            if abs(lv - clusters[-1][-1]) / clusters[-1][-1] <= tol:
                clusters[-1].append(lv)
            else:
                clusters.append([lv])
        return [round(np.mean(c), 2) for c in clusters]

    all_resistances = [l for l in cluster(pivot_highs) if l > close]
    all_supports    = [l for l in cluster(pivot_lows)  if l < close]

    nearest_resistance = min(all_resistances, default=None, key=lambda x: abs(x - close))
    nearest_support    = max(all_supports,    default=None, key=lambda x: abs(x - close))

    # Jarak ke level kunci (%)
    dist_resistance = _pct(nearest_resistance, close) if nearest_resistance else None
    dist_support    = _pct(nearest_support,    close) if nearest_support    else None

    # 52-week high & low
    high_52w = round(float(df["High"].tail(252).max()), 2)
    low_52w  = round(float(df["Low"].tail(252).min()),  2)

    return {
        "nearest_resistance":   nearest_resistance,
        "nearest_support":      nearest_support,
        "dist_resistance_pct":  dist_resistance,
        "dist_support_pct":     dist_support,
        "high_52w":             high_52w,
        "low_52w":              low_52w,
        "all_resistances":      all_resistances[-5:],   # 5 terdekat di atas
        "all_supports":         all_supports[:5],        # 5 terdekat di bawah
    }


# ─────────────────────────────────────────────────────────────────────────────
# BREAKOUT DETECTION
# ─────────────────────────────────────────────────────────────────────────────

def detect_breakout(df: pd.DataFrame, sr: dict) -> dict:
    """
    Deteksi apakah candle terakhir breakout dari level resistance kunci.
    Cek: harga close > resistance + volume surge konfirmasi.
    """
    close      = float(df["Close"].iloc[-1])
    prev_close = float(df["Close"].iloc[-2])
    volume     = float(df["Volume"].iloc[-1])
    vol_avg    = float(df["Volume"].tail(INDICATORS["volume_avg_days"] + 1).iloc[:-1].mean())
    vol_ratio  = round(volume / vol_avg, 2) if vol_avg > 0 else 0

    breakout_type   = "none"
    breakout_level  = None
    breakout_pct    = 0.0
    is_breakout     = False

    resistance = sr.get("nearest_resistance")
    high_52w   = sr.get("high_52w")

    # ① Breakout dari nearest resistance
    if resistance and prev_close <= resistance <= close:
        breakout_type  = "resistance_breakout"
        breakout_level = resistance
        breakout_pct   = _pct(close, resistance)
        is_breakout    = True

    # ② Breakout 52-week high (lebih kuat!)
    elif high_52w and close >= high_52w * 0.998:
        breakout_type  = "52w_high_breakout"
        breakout_level = high_52w
        breakout_pct   = _pct(close, high_52w)
        is_breakout    = True

    # ③ Near breakout (dalam 0.5% dari resistance)
    elif resistance and _pct(resistance, close) <= 0.5:
        breakout_type  = "near_breakout"
        breakout_level = resistance
        breakout_pct   = _pct(resistance, close)
        is_breakout    = False  # Belum breakout, tapi dekat

    return {
        "is_breakout":     is_breakout,
        "breakout_type":   breakout_type,
        "breakout_level":  breakout_level,
        "breakout_pct":    breakout_pct,
        "volume":          int(volume),
        "vol_avg_20d":     int(vol_avg),
        "vol_ratio":       vol_ratio,
        "volume_confirmed": vol_ratio >= INDICATORS.get("volume_surge_min", 1.5),
    }


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ANALYSIS FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

def compute_indicators(df: pd.DataFrame, ticker: str = "") -> Optional[dict]:
    """
    Hitung semua indikator teknikal dan kembalikan sebagai dict terstruktur.
    """
    try:
        cfg  = INDICATORS
        close = df["Close"]
        high  = df["High"]
        low   = df["Low"]
        vol   = df["Volume"]
        n     = len(df)

        result = {"ticker": ticker, "rows": n}

        # ── Harga ────────────────────────────────────────────────────────────
        result["price"] = {
            "close":       _safe_val(close),
            "open":        _safe_val(df["Open"]),
            "high":        _safe_val(high),
            "low":         _safe_val(low),
            "prev_close":  _safe_val(close, -2),
            "change_pct":  _pct(_safe_val(close), _safe_val(close, -2)),
        }

        # ── EMA ───────────────────────────────────────────────────────────────
        ema9   = ta.ema(close, length=cfg["ema_fast"])
        ema21  = ta.ema(close, length=cfg["ema_mid"])
        ema50  = ta.ema(close, length=cfg["ema_slow"])
        ema200 = ta.ema(close, length=cfg["ema_trend"])

        e9, e21, e50, e200 = (_safe_val(ema9), _safe_val(ema21),
                               _safe_val(ema50), _safe_val(ema200))

        # Cek susunan EMA bullish: 9 > 21 > 50 > 200
        ema_bullish = (e9 and e21 and e50 and e200 and
                       e9 > e21 > e50 > e200)
        ema_above_200 = (_safe_val(close) or 0) > (e200 or 0) if e200 else False

        result["ema"] = {
            "ema9": e9, "ema21": e21, "ema50": e50, "ema200": e200,
            "bullish_alignment": ema_bullish,
            "price_above_200":   ema_above_200,
            "ema9_vs_21_pct":    _pct(e9, e21) if e9 and e21 else None,
        }

        # ── SMA ───────────────────────────────────────────────────────────────
        sma20 = ta.sma(close, length=20)
        sma50 = ta.sma(close, length=50)
        result["sma"] = {
            "sma20": _safe_val(sma20),
            "sma50": _safe_val(sma50),
        }

        # ── RSI ───────────────────────────────────────────────────────────────
        rsi  = ta.rsi(close, length=cfg["rsi_period"])
        rsi_val  = _safe_val(rsi)
        rsi_prev = _safe_val(rsi, -2)

        rsi_zone = "overbought" if (rsi_val or 0) > 70 else (
                   "oversold"   if (rsi_val or 0) < 30 else
                   "bullish"    if (rsi_val or 0) >= 50 else "bearish")

        result["rsi"] = {
            "value":     rsi_val,
            "prev":      rsi_prev,
            "direction": "up" if rsi_val and rsi_prev and rsi_val > rsi_prev else "down",
            "zone":      rsi_zone,
        }

        # ── MACD ──────────────────────────────────────────────────────────────
        macd_df = ta.macd(close,
                          fast=cfg["macd_fast"],
                          slow=cfg["macd_slow"],
                          signal=cfg["macd_signal"])
        macd_col  = f"MACD_{cfg['macd_fast']}_{cfg['macd_slow']}_{cfg['macd_signal']}"
        sig_col   = f"MACDs_{cfg['macd_fast']}_{cfg['macd_slow']}_{cfg['macd_signal']}"
        hist_col  = f"MACDh_{cfg['macd_fast']}_{cfg['macd_slow']}_{cfg['macd_signal']}"

        macd_val  = _safe_val(macd_df[macd_col]) if macd_col in macd_df.columns else None
        sig_val   = _safe_val(macd_df[sig_col])  if sig_col  in macd_df.columns else None
        hist_val  = _safe_val(macd_df[hist_col]) if hist_col in macd_df.columns else None
        hist_prev = _safe_val(macd_df[hist_col], -2) if hist_col in macd_df.columns else None

        macd_cross = (macd_val and sig_val and
                      macd_val > sig_val and
                      _safe_val(macd_df[macd_col], -2) <= _safe_val(macd_df[sig_col], -2))
        hist_growing = (hist_val and hist_prev and hist_val > hist_prev and hist_val > 0)

        result["macd"] = {
            "macd":         macd_val,
            "signal":       sig_val,
            "histogram":    hist_val,
            "hist_prev":    hist_prev,
            "bullish_cross": macd_cross,
            "histogram_growing": hist_growing,
            "above_zero":   (macd_val or 0) > 0,
        }

        # ── Bollinger Bands ───────────────────────────────────────────────────
        bb = ta.bbands(close, length=cfg["bbands_period"], std=cfg["bbands_std"])
        bb_lower_col = f"BBL_{cfg['bbands_period']}_{float(cfg['bbands_std'])}"
        bb_mid_col   = f"BBM_{cfg['bbands_period']}_{float(cfg['bbands_std'])}"
        bb_upper_col = f"BBU_{cfg['bbands_period']}_{float(cfg['bbands_std'])}"
        bb_bw_col    = f"BBB_{cfg['bbands_period']}_{float(cfg['bbands_std'])}"

        def _bb(col): return _safe_val(bb[col]) if col in bb.columns else None

        bbu   = _bb(bb_upper_col)
        bbm   = _bb(bb_mid_col)
        bbl   = _bb(bb_lower_col)
        bb_bw = _bb(bb_bw_col)

        # Deteksi Bollinger Squeeze: bandwidth di 20-period low
        bw_series = bb[bb_bw_col] if bb_bw_col in bb.columns else None
        bw_min20  = float(bw_series.tail(20).min()) if bw_series is not None else None
        squeeze   = (bb_bw and bw_min20 and bb_bw <= bw_min20 * 1.05)

        close_val = _safe_val(close)
        result["bbands"] = {
            "upper":       bbu,
            "mid":         bbm,
            "lower":       bbl,
            "bandwidth":   bb_bw,
            "squeeze":     squeeze,
            "price_above_upper": (close_val or 0) > (bbu or float("inf")),
            "price_above_mid":   (close_val or 0) > (bbm or 0),
        }

        # ── ATR ───────────────────────────────────────────────────────────────
        atr     = ta.atr(high, low, close, length=cfg["atr_period"])
        atr_val = _safe_val(atr)
        result["atr"] = {
            "value": atr_val,
            "pct_of_price": _pct(atr_val, close_val) if atr_val and close_val else None,
        }

        # ── Stochastic ────────────────────────────────────────────────────────
        stoch    = ta.stoch(high, low, close, k=cfg["stoch_k"], d=cfg["stoch_d"])
        stoch_k  = _safe_val(stoch.iloc[:, 0]) if stoch is not None else None
        stoch_d  = _safe_val(stoch.iloc[:, 1]) if stoch is not None else None

        result["stochastic"] = {
            "k":          stoch_k,
            "d":          stoch_d,
            "bullish_cross": (stoch_k and stoch_d and stoch_k > stoch_d and
                              stoch_k < 80),  # Cross tapi belum overbought
            "oversold":   (stoch_k or 100) < 20,
        }

        # ── MFI (Money Flow Index) ────────────────────────────────────────────
        mfi     = ta.mfi(high, low, close, vol, length=cfg["mfi_period"])
        mfi_val = _safe_val(mfi)

        result["mfi"] = {
            "value":      mfi_val,
            "zone":       ("overbought" if (mfi_val or 0) > 80 else
                           "oversold"   if (mfi_val or 0) < 20 else
                           "bullish"    if (mfi_val or 0) >= 50 else "bearish"),
        }

        # ── OBV ───────────────────────────────────────────────────────────────
        obv      = ta.obv(close, vol)
        obv_ema  = ta.ema(obv, length=cfg["obv_ema"])
        obv_val  = _safe_val(obv)
        obve_val = _safe_val(obv_ema)

        result["obv"] = {
            "value":          obv_val,
            "ema":            obve_val,
            "above_ema":      (obv_val or 0) > (obve_val or 0),
            "rising":         _safe_val(obv) and _safe_val(obv, -2) and obv_val > _safe_val(obv, -2),
        }

        # ── VWAP ──────────────────────────────────────────────────────────────
        # Untuk EOD, kita hitung VWAP manual untuk 20 hari terakhir
        recent_df  = df.tail(20)
        typical_p  = (recent_df["High"] + recent_df["Low"] + recent_df["Close"]) / 3
        vwap_val   = round(float((typical_p * recent_df["Volume"]).sum() /
                                  recent_df["Volume"].sum()), 2)
        result["vwap"] = {
            "value_20d":    vwap_val,
            "price_above":  (close_val or 0) > vwap_val,
        }

        # ── Volume Analysis ───────────────────────────────────────────────────
        vol_today   = float(vol.iloc[-1])
        vol_avg20   = float(vol.tail(INDICATORS["volume_avg_days"] + 1).iloc[:-1].mean())
        vol_ratio   = round(vol_today / vol_avg20, 2) if vol_avg20 > 0 else 0

        result["volume"] = {
            "today":         int(vol_today),
            "avg_20d":       int(vol_avg20),
            "ratio":         vol_ratio,
            "surge":         vol_ratio >= 1.5,
            "extreme_surge": vol_ratio >= 3.0,
        }

        # ── Support & Resistance ─────────────────────────────────────────────
        sr = detect_support_resistance(df)
        result["sr"] = sr

        # ── Breakout Detection ───────────────────────────────────────────────
        bo = detect_breakout(df, sr)
        result["breakout"] = bo

        return result

    except Exception as e:
        logger.error(f"[{ticker}] Error compute_indicators: {e}", exc_info=True)
        return None
