"""
bot_handler.py — Handle perintah chat dari Telegram
"""

import logging
import os
import sys
import threading
import time
import requests

os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/bot.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv()

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, WATCHLIST, SECTORS
from data_fetcher import fetch_ohlcv
from technical_analysis import compute_indicators
from ai_scorer import analyze_with_ai
from sector_info import get_sector_info_message, get_all_sectors_list

API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
offset = 0


def get_updates():
    global offset
    try:
        r = requests.get(
            f"{API}/getUpdates",
            params={"timeout": 30, "offset": offset},
            timeout=35,
        )
        data = r.json()
        if data.get("ok"):
            return data.get("result", [])
    except Exception as e:
        logger.error(f"getUpdates error: {e}")
    return []


def reply(chat_id, text):
    try:
        requests.post(
            f"{API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
            timeout=15,
        )
    except Exception as e:
        logger.error(f"Reply error: {e}")


def send_inline_keyboard(chat_id, text, buttons):
    try:
        requests.post(
            f"{API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
                "reply_markup": {"inline_keyboard": buttons},
            },
            timeout=15,
        )
    except Exception as e:
        logger.error(f"Inline keyboard error: {e}")


def format_result(tech, ai):
    ticker  = ai.get("ticker", "")
    score   = ai.get("score", 0)
    signal  = ai.get("signal", "")
    conf    = ai.get("confidence", "")
    summary = ai.get("summary", "")

    price  = tech.get("price", {})
    rsi    = tech.get("rsi", {})
    macd   = tech.get("macd", {})
    ema    = tech.get("ema", {})
    volume = tech.get("volume", {})
    bo     = tech.get("breakout", {})
    sr     = tech.get("sr", {})
    rm     = ai.get("risk_management", {})
    entry  = ai.get("entry_zone", {})
    warns  = ai.get("warnings", [])
    cats   = ai.get("catalysts", [])

    signal_emoji = {"STRONG_BUY": "🚀", "BUY": "📈", "NEUTRAL": "⚖️", "AVOID": "🚫"}.get(signal, "❓")
    conf_badge   = {"HIGH": "🟢 HIGH", "MEDIUM": "🟡 MEDIUM", "LOW": "🔴 LOW"}.get(conf, conf)

    filled = round(score / 10)
    bar    = "█" * filled + "░" * (10 - filled)
    chg    = price.get("change_pct", 0)
    chg_arrow = "🔺" if (chg or 0) >= 0 else "🔻"

    try:
        harga = f"{float(price.get('close', 0)):,.0f}"
    except Exception:
        harga = str(price.get("close", "-"))

    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"{signal_emoji} <b>ANALISA {ticker}</b>",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        f"💰 Harga: <b>{harga}</b> {chg_arrow} {chg}%",
        f"📅 Tanggal: {price.get('date', '-')}",
        "",
        f"🎯 Sinyal: <b>{signal}</b>  {conf_badge}",
        f"📊 Score: <code>{bar} {score}/100</code>",
        "",
        f"💬 <i>{summary}</i>",
        "",
        "─────────────────────────────",
        "🔬 <b>INDIKATOR</b>",
        f"  • RSI(14): <b>{rsi.get('value')}</b> — {rsi.get('zone')}",
        f"  • MACD Cross: {'✅' if macd.get('bullish_cross') else '❌'}  |  Hist: {'✅' if macd.get('histogram_growing') else '❌'}",
        f"  • EMA Bullish: {'✅' if ema.get('bullish_alignment') else '❌'}  |  >EMA200: {'✅' if ema.get('price_above_200') else '❌'}",
        f"  • Volume: {volume.get('ratio')}x avg {'🔥' if volume.get('surge') else ''}",
        "",
        "─────────────────────────────",
        "🚨 <b>BREAKOUT</b>",
        f"  • Tipe: {bo.get('breakout_type', '-')}",
        f"  • Level: {bo.get('breakout_level', '-')}",
        f"  • Resistance: {sr.get('nearest_resistance', '-')}",
        f"  • Support: {sr.get('nearest_support', '-')}",
        f"  • 52W High: {sr.get('high_52w', '-')}",
        "",
        "─────────────────────────────",
        "🎯 <b>ENTRY &amp; RISK MANAGEMENT</b>",
        f"  • Entry Zone: {entry.get('entry_range_low')} — {entry.get('entry_range_high')}",
        f"  • Stop Loss: {rm.get('stop_loss')} ({rm.get('stop_loss_pct')}%)",
        f"  • Target 1: {rm.get('target_1')} (+{rm.get('target_1_pct')}%)",
        f"  • Target 2: {rm.get('target_2')} (+{rm.get('target_2_pct')}%)",
        f"  • Risk/Reward: {rm.get('risk_reward_ratio')}:1",
        f"  • Timeframe: {ai.get('timeframe', '-')}",
        "",
    ]

    if cats:
        lines.append("✨ <b>FAKTOR POSITIF</b>")
        for c in cats[:3]:
            lines.append(f"  + {c}")
        lines.append("")

    if warns:
        lines.append("⚠️ <b>PERINGATAN</b>")
        for w in warns[:3]:
            lines.append(f"  ! {w}")
        lines.append("")

    lines += [
        "─────────────────────────────",
        "🤖 <i>Stock Bot IDX | Powered by Groq AI</i>",
        "⚠️ <i>Bukan rekomendasi investasi. DYOR!</i>",
    ]

    return "\n".join(lines)


def handle_cek(chat_id, ticker):
    if not ticker.endswith(".JK"):
        ticker = ticker + ".JK"
    ticker = ticker.upper()

    reply(chat_id, f"🔍 Menganalisa <b>{ticker}</b>...\nMohon tunggu 10-15 detik.")

    df = fetch_ohlcv(ticker)
    if df is None:
        reply(chat_id, f"❌ Tidak bisa ambil data {ticker}.\nPastikan ticker benar. Contoh: BBCA, TLKM, ANTM")
        return

    tech = compute_indicators(df, ticker=ticker)
    if tech is None:
        reply(chat_id, f"❌ Gagal hitung indikator untuk {ticker}.")
        return

    reply(chat_id, "🤖 Data siap, AI sedang menganalisa...")

    ai = analyze_with_ai(tech)
    if ai is None:
        reply(chat_id, f"❌ AI gagal menganalisa {ticker}. Coba lagi.")
        return

    msg = format_result(tech, ai)
    reply(chat_id, msg)


def handle_scan(chat_id, tickers=None):
    target = tickers if tickers else WATCHLIST
    total  = len(target)

    reply(chat_id, f"🔍 Memulai scan <b>{total} saham</b>...\nBot akan diam selama proses, hasil dikirim setelah selesai.")

    results = []
    for i, t in enumerate(target, 1):
        ticker = t.upper()
        if not ticker.endswith(".JK"):
            ticker += ".JK"

        if i % 50 == 0:
            reply(chat_id, f"⏳ Progress: {i}/{total} saham diproses...")

        df = fetch_ohlcv(ticker)
        if df is None:
            continue

        tech = compute_indicators(df, ticker=ticker)
        if tech is None:
            continue

        bo  = tech.get("breakout", {})
        vol = tech.get("volume", {})
        ema = tech.get("ema", {})

        has_potential = (
            bo.get("is_breakout") or
            bo.get("breakout_type") == "near_breakout" or
            (vol.get("surge") and ema.get("price_above_200"))
        )

        if not has_potential:
            continue

        ai = analyze_with_ai(tech)
        if ai is None:
            continue

        results.append({
            "ticker": ticker,
            "score":  ai.get("score", 0),
            "signal": ai.get("signal", ""),
            "tech":   tech,
            "ai":     ai,
        })

        time.sleep(1)

    if not results:
        reply(chat_id, "📊 Scan selesai.\n\nTidak ada saham yang memenuhi kriteria breakout hari ini.")
        return

    results.sort(key=lambda x: x["score"], reverse=True)
    summary_lines = ["📊 <b>HASIL SCAN</b>", ""]
    for r in results:
        sig_e = {"STRONG_BUY": "🚀", "BUY": "📈", "NEUTRAL": "⚖️", "AVOID": "🚫"}.get(r["signal"], "")
        summary_lines.append(f"{sig_e} <b>{r['ticker']}</b> — {r['score']}/100 — {r['signal']}")
    summary_lines += ["", f"Total: {len(results)} saham potensial"]
    reply(chat_id, "\n".join(summary_lines))

    time.sleep(2)
    for r in results:
        if r["score"] >= 55:
            msg = format_result(r["tech"], r["ai"])
            reply(chat_id, msg)
            time.sleep(2)


def handle_sektor(chat_id, nama_sektor):
    if not nama_sektor:
        sektor_list = "\n".join([f"  • /sektor {s}" for s in SECTORS.keys()])
        reply(chat_id,
            f"📂 <b>DAFTAR SEKTOR TERSEDIA</b>\n\n{sektor_list}\n\n"
            f"Contoh: <code>/sektor energi</code>\n"
            f"Info emiten: <code>/info energi</code>"
        )
        return

    nama_sektor = nama_sektor.lower().strip()

    if nama_sektor not in SECTORS:
        sektor_list = ", ".join(SECTORS.keys())
        reply(chat_id,
            f"❌ Sektor <b>{nama_sektor}</b> tidak ditemukan.\n\n"
            f"Tersedia: {sektor_list}"
        )
        return

    tickers = SECTORS[nama_sektor]
    reply(chat_id,
        f"🔍 Scanning sektor <b>{nama_sektor.upper()}</b>\n"
        f"📊 Total: {len(tickers)} saham\n"
        f"⏱ Estimasi: ~{len(tickers) * 3} detik..."
    )
    threading.Thread(target=handle_scan, args=(chat_id, tickers), daemon=True).start()


def handle_info(chat_id, nama_sektor):
    if not nama_sektor:
        msg = get_all_sectors_list()
        reply(chat_id, msg)
        return
    nama_sektor = nama_sektor.lower().strip()
    msg = get_sector_info_message(nama_sektor)
    reply(chat_id, msg)


def handle_watchlist(chat_id):
    lines = ["📋 <b>WATCHLIST AKTIF</b>", ""]
    for i, t in enumerate(WATCHLIST, 1):
        lines.append(f"{i}. {t}")
    lines += ["", f"Total: {len(WATCHLIST)} saham"]
    reply(chat_id, "\n".join(lines))


def handle_help(chat_id):
    msg = """╔════════════════════════════╗
║  🤖  <b>STOCK BOT IDX</b>  📈        ║
║  <i>Powered by Groq AI</i>           ║
╚════════════════════════════╝

━━━━━━  📌 <b>PERINTAH UTAMA</b>  ━━━━━━

🔍 <b>/cek</b> <code>BBCA</code>
    └ Analisa mendalam satu saham

🔍 <b>/cek</b> <code>BBCA TLKM ANTM</code>
    └ Analisa beberapa saham sekaligus

📡 <b>/scan</b>
    └ Scan seluruh watchlist

📡 <b>/scan</b> <code>BBCA TLKM</code>
    └ Scan saham pilihan

🏭 <b>/sektor</b> <code>energi</code>
    └ Scan breakout per sektor

📂 <b>/info</b>
    └ Lihat daftar semua sektor

📂 <b>/info</b> <code>konglomerat</code>
    └ Detail emiten per grup konglomerat

📂 <b>/info</b> <code>catalyst</code>
    └ Narasi &amp; katalis saham panas 2026

📋 <b>/watchlist</b>
    └ Lihat daftar semua saham

━━━━━━  🏭 <b>SEKTOR TERSEDIA</b>  ━━━━━━

🏢 konglomerat   ⚡ energi
⛏️ tambang        🏠 properti
🏗️ infrastruktur  ⚓ perkapalan
💻 teknologi     🛒 consumer
🏥 kesehatan     🌴 agribisnis
📡 telko         🛍️ retail
📺 media         🔋 ev
🔥 catalyst

━━━━━━  💡 <b>CONTOH</b>  ━━━━━━

▶️ <code>/info catalyst</code> — narasi saham panas
▶️ <code>/info konglomerat</code> — grup konglomerat
▶️ <code>/sektor tambang</code> — scan breakout tambang
▶️ <code>/cek AMMN</code> — analisa saham

╔════════════════════════════╗
║ ⚠️ <i>Bukan rekomendasi investasi</i> ║
║    <i>Lakukan riset mandiri. DYOR!</i> ║
╚════════════════════════════╝"""
    reply(chat_id, msg)


def process_update(update):
    global offset
    offset = update["update_id"] + 1

    # Handle tombol inline keyboard
    callback = update.get("callback_query", {})
    if callback:
        cid   = str(callback.get("message", {}).get("chat", {}).get("id", ""))
        data  = callback.get("data", "")
        cb_id = callback.get("id", "")
        requests.post(f"{API}/answerCallbackQuery", json={"callback_query_id": cb_id}, timeout=5)
        if data == "menu_cek":
            reply(cid, "🔍 Ketik perintah:\n<code>/cek BBCA</code>\natau\n<code>/cek BBCA TLKM ANTM</code>")
        elif data == "menu_scan":
            threading.Thread(target=handle_scan, args=(cid, None), daemon=True).start()
        elif data == "menu_sektor":
            handle_sektor(cid, "")
        elif data == "menu_info":
            handle_info(cid, "")
        elif data == "menu_watchlist":
            handle_watchlist(cid)
        elif data == "menu_help":
            handle_help(cid)
        return

    msg = update.get("message", {})
    if not msg:
        return

    chat_id = str(msg.get("chat", {}).get("id", ""))
    text    = msg.get("text", "").strip()

    if not text:
        return

    logger.info(f"Pesan masuk dari {chat_id}: {text}")

    parts = text.split()
    cmd   = parts[0].lower().split("@")[0]

    if cmd == "/start":
        welcome = """╔═══════════════════════════╗
║  🤖  <b>STOCK BOT IDX</b>  📈      ║
║  <i>Powered by Groq AI</i>          ║
╚═══════════════════════════╝

👋 <b>Selamat datang!</b>

Bot ini membantu kamu menganalisa saham IDX secara otomatis menggunakan AI dan indikator teknikal.

✨ <b>Yang bisa bot ini lakukan:</b>
  📊 Analisa teknikal mendalam
  📡 Scan breakout &amp; sinyal
  🏭 Filter per sektor saham
  📂 Info emiten &amp; narasi katalyst
  🎯 Entry, SL &amp; Target otomatis

⚡ <i>Pilih menu di bawah untuk mulai:</i>"""

        buttons = [
            [
                {"text": "🔍 Cek Saham", "callback_data": "menu_cek"},
                {"text": "📡 Scan Watchlist", "callback_data": "menu_scan"},
            ],
            [
                {"text": "🏭 Scan Sektor", "callback_data": "menu_sektor"},
                {"text": "📂 Info Sektor", "callback_data": "menu_info"},
            ],
            [
                {"text": "📋 Watchlist", "callback_data": "menu_watchlist"},
                {"text": "❓ Help", "callback_data": "menu_help"},
            ],
        ]
        send_inline_keyboard(chat_id, welcome, buttons)

    elif cmd == "/help":
        handle_help(chat_id)

    elif cmd == "/watchlist":
        handle_watchlist(chat_id)

    elif cmd == "/sektor":
        nama = parts[1] if len(parts) > 1 else ""
        handle_sektor(chat_id, nama)

    elif cmd == "/info":
        nama = parts[1] if len(parts) > 1 else ""
        handle_info(chat_id, nama)

    elif cmd == "/cek":
        if len(parts) < 2:
            reply(chat_id, "❌ Format salah!\nContoh: /cek BBCA")
            return
        tickers = parts[1:]
        for t in tickers:
            threading.Thread(target=handle_cek, args=(chat_id, t), daemon=True).start()
            time.sleep(0.5)

    elif cmd == "/scan":
        tickers = parts[1:] if len(parts) > 1 else None
        threading.Thread(target=handle_scan, args=(chat_id, tickers), daemon=True).start()

    else:
        reply(chat_id, "❓ Perintah tidak dikenal.\nKetik /help untuk melihat menu.")


def main():
    logger.info("=" * 50)
    logger.info("  STOCK BOT IDX — Chat Handler Aktif")
    logger.info("  Kirim /help ke bot Telegram kamu")
    logger.info("=" * 50)

    reply(TELEGRAM_CHAT_ID,
        "🤖 <b>Stock Bot IDX aktif!</b>\n\nKetik /help untuk melihat semua perintah.")

    logger.info("Menunggu pesan dari Telegram... (Ctrl+C untuk berhenti)")

    while True:
        try:
            updates = get_updates()
            for update in updates:
                process_update(update)
        except KeyboardInterrupt:
            logger.info("Bot dihentikan.")
            break
        except Exception as e:
            logger.error(f"Error main loop: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()
