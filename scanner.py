"""
scanner.py — Orkestrasi pipeline analisa saham IDX
Flow: Fetch Data → Hitung Indikator → AI Scoring → Filter → Telegram Alert
"""

import logging
import time
from typing import Optional
from config import WATCHLIST, MIN_SCORE
from data_fetcher import fetch_ohlcv
from technical_analysis import compute_indicators
from ai_scorer import analyze_with_ai, should_send_alert
from telegram_notifier import send_alert, send_error_notification, format_summary_message, send_message
from cooldown_manager import is_on_cooldown, mark_sent, clear_expired

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# SINGLE TICKER PIPELINE
# ─────────────────────────────────────────────────────────────────────────────

def analyze_ticker(ticker: str) -> Optional[dict]:
    """
    Jalankan pipeline lengkap untuk satu ticker.
    Return dict hasil atau None jika ada error.
    """
    result = {
        "ticker":     ticker,
        "score":      0,
        "signal":     "NEUTRAL",
        "alert_sent": False,
        "skip_reason": None,
    }

    # ① Cek cooldown
    if is_on_cooldown(ticker):
        result["skip_reason"] = "cooldown"
        return result

    # ② Fetch OHLCV
    df = fetch_ohlcv(ticker)
    if df is None:
        logger.warning(f"[{ticker}] Tidak dapat fetch data, skip")
        result["skip_reason"] = "fetch_error"
        return result

    # ③ Hitung indikator teknikal
    tech_data = compute_indicators(df, ticker=ticker)
    if tech_data is None:
        logger.warning(f"[{ticker}] Gagal hitung indikator, skip")
        result["skip_reason"] = "indicator_error"
        return result

    # ④ Pre-filter: skip kalau tidak ada signal breakout sama sekali
    bo = tech_data.get("breakout", {})
    vol = tech_data.get("volume", {})
    ema = tech_data.get("ema", {})

    # Minimal harus ada salah satu sinyal yang menjanjikan
    has_potential = (
        bo.get("is_breakout") or
        bo.get("breakout_type") == "near_breakout" or
        (vol.get("surge") and ema.get("price_above_200"))
    )

    if not has_potential:
        logger.debug(f"[{ticker}] Tidak ada potensi breakout, skip AI scoring")
        result["skip_reason"] = "no_potential"
        return result

    # ⑤ AI Scoring dengan Claude
    logger.info(f"[{ticker}] Mengirim ke AI untuk scoring...")
    ai_result = analyze_with_ai(tech_data)
    if ai_result is None:
        logger.warning(f"[{ticker}] AI scoring gagal, skip")
        result["skip_reason"] = "ai_error"
        return result

    result["score"]  = ai_result.get("score", 0)
    result["signal"] = ai_result.get("signal", "NEUTRAL")

    # ⑥ Cek apakah layak dikirim alert
    if not should_send_alert(ai_result):
        logger.info(
            f"[{ticker}] Score {result['score']}/100 di bawah threshold {MIN_SCORE}, "
            f"sinyal: {result['signal']} — tidak dikirim"
        )
        result["skip_reason"] = f"score_below_threshold ({result['score']}/{MIN_SCORE})"
        return result

    # ⑦ Kirim alert ke Telegram
    logger.info(f"[{ticker}] 🚀 ALERT! Score {result['score']}/100 — {result['signal']}")
    sent = send_alert(tech_data, ai_result)

    if sent:
        mark_sent(ticker, score=result["score"], signal=result["signal"])
        result["alert_sent"] = True
        logger.info(f"[{ticker}] ✅ Alert berhasil dikirim ke Telegram")
    else:
        logger.error(f"[{ticker}] ❌ Gagal kirim alert ke Telegram")

    return result


# ─────────────────────────────────────────────────────────────────────────────
# FULL SCAN
# ─────────────────────────────────────────────────────────────────────────────

def run_full_scan(watchlist: list = None, delay_between: float = 1.5) -> list:
    """
    Scan semua ticker dalam watchlist.
    Return list hasil analisa.
    """
    tickers = watchlist or WATCHLIST
    total   = len(tickers)
    results = []

    logger.info(f"{'='*50}")
    logger.info(f"🔍 MULAI SCAN EOD — {total} saham IDX")
    logger.info(f"{'='*50}")

    # Bersihkan cooldown kadaluarsa sebelum scan
    removed = clear_expired()
    if removed:
        logger.info(f"Cleaned {removed} expired cooldown entries")

    for i, ticker in enumerate(tickers, 1):
        logger.info(f"[{i}/{total}] Analyzing {ticker}...")
        try:
            result = analyze_ticker(ticker)
            if result:
                results.append(result)
        except Exception as e:
            logger.error(f"[{ticker}] Unexpected error: {e}", exc_info=True)
            results.append({
                "ticker":     ticker,
                "score":      0,
                "signal":     "ERROR",
                "alert_sent": False,
                "skip_reason": f"unexpected_error: {str(e)[:100]}",
            })

        # Rate limiting: jangan spam Yahoo Finance & Anthropic API
        if i < total:
            time.sleep(delay_between)

    # ── Ringkasan Scan ────────────────────────────────────────────────────────
    alerts_sent  = [r for r in results if r.get("alert_sent")]
    errors       = [r for r in results if r and  r.get("skip_reason", "").startswith("unexpected")]

    logger.info(f"{'='*50}")
    logger.info(f"📊 SCAN SELESAI")
    logger.info(f"   Total dipindai : {total}")
    logger.info(f"   Alert dikirim  : {len(alerts_sent)}")
    logger.info(f"   Error          : {len(errors)}")
    if alerts_sent:
        logger.info(f"   Saham alert    : {[r['ticker'] for r in alerts_sent]}")
    logger.info(f"{'='*50}")

    # Kirim ringkasan ke Telegram
    try:
        summary_msg = format_summary_message(results)
        send_message(summary_msg)
    except Exception as e:
        logger.error(f"Gagal kirim summary: {e}")

    return results


# ─────────────────────────────────────────────────────────────────────────────
# SKIP REASON REPORT
# ─────────────────────────────────────────────────────────────────────────────

def print_scan_report(results: list) -> None:
    """Print laporan scan ke console."""
    from collections import Counter
    skip_reasons = Counter(
        r.get("skip_reason", "none")
        for r in results
        if not r.get("alert_sent")
    )

    print("\n── SKIP REASONS ──")
    for reason, count in skip_reasons.most_common():
        print(f"  {reason}: {count}")

    print("\n── ALERTS SENT ──")
    for r in sorted(results, key=lambda x: x.get("score", 0), reverse=True):
        if r.get("alert_sent"):
            print(f"  {r['ticker']}: {r['score']}/100 — {r['signal']}")
