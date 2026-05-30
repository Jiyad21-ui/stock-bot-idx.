"""
main.py — Entry point utama Stock Breakout Bot IDX
Jalankan: python main.py
Bot akan scan setiap hari setelah penutupan IDX (default 15:45 WIB)
"""

import logging
import os
import sys
from datetime import datetime

# ─── Setup logging sebelum import lainnya ────────────────────────────────────
os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/bot.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

# ─── Import setelah logging siap ─────────────────────────────────────────────
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from config import SCAN_TIME_WIB, WATCHLIST
from scanner import run_full_scan
from telegram_notifier import send_startup_message, send_message, send_error_notification


# ─────────────────────────────────────────────────────────────────────────────
# SCHEDULED JOB
# ─────────────────────────────────────────────────────────────────────────────

def scheduled_scan():
    """Job yang dijalankan scheduler setiap hari."""
    now = datetime.now(pytz.timezone("Asia/Jakarta"))
    logger.info(f"⏰ Scheduled scan dimulai: {now.strftime('%Y-%m-%d %H:%M:%S WIB')}")

    # Skip weekend (Sabtu=5, Minggu=6) — IDX tidak buka
    if now.weekday() >= 5:
        logger.info(f"⏭️ Hari ini {now.strftime('%A')} — IDX libur, scan dilewati")
        return

    try:
        results = run_full_scan()
        logger.info(f"✅ Scan selesai. {len([r for r in results if r.get('alert_sent')])} alert dikirim.")
    except Exception as e:
        logger.error(f"❌ Error saat scan: {e}", exc_info=True)
        send_error_notification(str(e))


# ─────────────────────────────────────────────────────────────────────────────
# MANUAL SCAN (untuk testing)
# ─────────────────────────────────────────────────────────────────────────────

def manual_scan(tickers: list = None):
    """Jalankan scan manual tanpa scheduler."""
    logger.info("🔧 MODE MANUAL SCAN")
    tickers = tickers or WATCHLIST
    results = run_full_scan(watchlist=tickers)
    return results


# ─────────────────────────────────────────────────────────────────────────────
# TELEGRAM COMMAND HANDLER (opsional, untuk /status /scan commands)
# ─────────────────────────────────────────────────────────────────────────────

def check_telegram_commands():
    """
    Cek perintah dari Telegram (polling sederhana).
    Untuk fitur lengkap, gunakan python-telegram-bot dengan handlers.
    """
    import requests
    from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

    try:
        resp = requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates",
            params={"timeout": 1, "limit": 5},
            timeout=5,
        )
        updates = resp.json().get("result", [])

        for update in updates:
            msg = update.get("message", {})
            text = msg.get("text", "")
            chat_id = str(msg.get("chat", {}).get("id", ""))

            # Hanya proses dari chat yang dikonfigurasi
            if chat_id != str(TELEGRAM_CHAT_ID):
                continue

            if text == "/status":
                from cooldown_manager import get_history
                history = get_history()
                count = len(history)
                send_message(
                    f"✅ *Bot aktif*\n"
                    f"📊 Watchlist: {len(WATCHLIST)} saham\n"
                    f"🕐 Jadwal scan: {SCAN_TIME_WIB} WIB\n"
                    f"📝 Cooldown aktif: {count} ticker",
                    chat_id=chat_id,
                )

            elif text.startswith("/scan"):
                parts = text.split()
                if len(parts) > 1:
                    # /scan BBCA.JK BBRI.JK
                    tickers = [t.upper() for t in parts[1:]]
                    if not all(t.endswith(".JK") for t in tickers):
                        tickers = [t if t.endswith(".JK") else t + ".JK" for t in tickers]
                    send_message(f"🔍 Scanning {', '.join(tickers)}...", chat_id=chat_id)
                    import threading
                    threading.Thread(target=manual_scan, args=(tickers,), daemon=True).start()
                else:
                    send_message(
                        "Usage: `/scan BBCA.JK BBRI.JK`\n"
                        "Atau `/scan` untuk scan semua watchlist",
                        chat_id=chat_id,
                    )

    except Exception as e:
        logger.debug(f"Command check error (diabaikan): {e}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    logger.info("=" * 60)
    logger.info("  STOCK BREAKOUT BOT IDX — Starting Up")
    logger.info(f"  Watchlist    : {len(WATCHLIST)} saham")
    logger.info(f"  Jadwal Scan  : {SCAN_TIME_WIB} WIB (Senin-Jumat)")
    logger.info("=" * 60)

    # Kirim notifikasi startup ke Telegram
    try:
        send_startup_message()
    except Exception as e:
        logger.warning(f"Tidak bisa kirim startup message: {e}")

    # Setup scheduler
    wib = pytz.timezone("Asia/Jakarta")
    hour, minute = SCAN_TIME_WIB.split(":")

    scheduler = BlockingScheduler(timezone=wib)

    # Job utama: scan EOD tiap hari Senin–Jumat
    scheduler.add_job(
        scheduled_scan,
        trigger=CronTrigger(
            day_of_week="mon-fri",
            hour=int(hour),
            minute=int(minute),
            timezone=wib,
        ),
        id="eod_scan",
        name="EOD Stock Scan IDX",
        misfire_grace_time=3600,  # toleransi 1 jam jika sempat mati
    )

    # Job ringan: cek command Telegram setiap 30 detik
    scheduler.add_job(
        check_telegram_commands,
        trigger="interval",
        seconds=30,
        id="telegram_commands",
        name="Telegram Command Listener",
    )

    logger.info(f"✅ Scheduler aktif. Menunggu jam {SCAN_TIME_WIB} WIB...")
    logger.info("   Tekan Ctrl+C untuk berhenti\n")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("🛑 Bot dihentikan oleh user")
        scheduler.shutdown()


if __name__ == "__main__":
    # Cek argumen command line
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()

        if cmd == "scan":
            # python main.py scan                → scan semua watchlist sekarang
            # python main.py scan BBCA.JK TLKM   → scan ticker tertentu
            tickers = [t.upper() for t in sys.argv[2:]] or None
            if tickers:
                tickers = [t if t.endswith(".JK") else t + ".JK" for t in tickers]
            results = manual_scan(tickers)
            from scanner import print_scan_report
            print_scan_report(results)

        elif cmd == "test":
            # python main.py test → test koneksi semua layanan
            logger.info("🧪 Menjalankan tes koneksi...")

            # Test Telegram
            from telegram_notifier import send_message
            ok = send_message("🧪 Test koneksi Bot OK\\!")
            logger.info(f"Telegram: {'✅ OK' if ok else '❌ GAGAL'}")

            # Test Yahoo Finance
            from data_fetcher import fetch_ohlcv
            df = fetch_ohlcv("BBCA.JK", period="5d")
            logger.info(f"Yahoo Finance: {'✅ OK' if df is not None else '❌ GAGAL'}")

            # Test Anthropic
            try:
                import anthropic
                from config import ANTHROPIC_API_KEY
                c = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
                r = c.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=10,
                    messages=[{"role": "user", "content": "hi"}],
                )
                logger.info("Anthropic API: ✅ OK")
            except Exception as e:
                logger.info(f"Anthropic API: ❌ GAGAL — {e}")

        else:
            print(f"Command tidak dikenal: {cmd}")
            print("Usage:")
            print("  python main.py            → jalankan scheduler")
            print("  python main.py scan       → scan semua watchlist sekarang")
            print("  python main.py scan BBCA  → scan ticker tertentu")
            print("  python main.py test       → test koneksi semua layanan")
    else:
        main()
