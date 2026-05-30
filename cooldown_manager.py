"""
cooldown_manager.py — Cegah spam alert untuk ticker yang sama
Simpan riwayat alert ke file JSON lokal
"""

import json
import logging
import os
from datetime import datetime, timedelta
from config import ALERT_COOLDOWN_DAYS, COOLDOWN_FILE

logger = logging.getLogger(__name__)


def _load_history() -> dict:
    """Load riwayat alert dari file JSON."""
    os.makedirs(os.path.dirname(COOLDOWN_FILE), exist_ok=True)
    if not os.path.exists(COOLDOWN_FILE):
        return {}
    try:
        with open(COOLDOWN_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.warning(f"Gagal baca cooldown file: {e}")
        return {}


def _save_history(history: dict) -> None:
    """Simpan riwayat alert ke file JSON."""
    try:
        os.makedirs(os.path.dirname(COOLDOWN_FILE), exist_ok=True)
        with open(COOLDOWN_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except IOError as e:
        logger.error(f"Gagal simpan cooldown file: {e}")


def is_on_cooldown(ticker: str) -> bool:
    """
    Cek apakah ticker masih dalam masa cooldown.
    Return True jika alert terakhir belum N hari yang lalu.
    """
    history = _load_history()
    if ticker not in history:
        return False

    last_sent_str = history[ticker].get("last_sent")
    if not last_sent_str:
        return False

    try:
        last_sent = datetime.fromisoformat(last_sent_str)
        cooldown_until = last_sent + timedelta(days=ALERT_COOLDOWN_DAYS)
        on_cooldown = datetime.now() < cooldown_until

        if on_cooldown:
            logger.info(
                f"[{ticker}] Masih cooldown hingga "
                f"{cooldown_until.strftime('%Y-%m-%d')} "
                f"(alert terakhir: {last_sent.strftime('%Y-%m-%d')})"
            )
        return on_cooldown
    except ValueError:
        return False


def mark_sent(ticker: str, score: int = 0, signal: str = "") -> None:
    """Tandai bahwa alert untuk ticker ini sudah dikirim hari ini."""
    history = _load_history()
    history[ticker] = {
        "last_sent":  datetime.now().isoformat(),
        "last_score": score,
        "last_signal": signal,
        "send_count": history.get(ticker, {}).get("send_count", 0) + 1,
    }
    _save_history(history)
    logger.info(f"[{ticker}] Marked as sent. Cooldown {ALERT_COOLDOWN_DAYS} hari.")


def get_history(ticker: str = None) -> dict:
    """Ambil riwayat alert. Jika ticker None, return semua riwayat."""
    history = _load_history()
    if ticker:
        return history.get(ticker, {})
    return history


def clear_expired() -> int:
    """
    Bersihkan entry yang sudah melewati cooldown period.
    Return jumlah entry yang dihapus.
    """
    history = _load_history()
    cutoff  = datetime.now() - timedelta(days=ALERT_COOLDOWN_DAYS * 2)
    expired = [
        t for t, v in history.items()
        if datetime.fromisoformat(v.get("last_sent", "2000-01-01")) < cutoff
    ]
    for t in expired:
        del history[t]
    if expired:
        _save_history(history)
        logger.info(f"Dihapus {len(expired)} entry cooldown kadaluarsa")
    return len(expired)
