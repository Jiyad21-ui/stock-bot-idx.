"""
telegram_notifier.py — Format dan kirim alert breakout ke Telegram
Pesan menggunakan Telegram MarkdownV2 dengan layout yang rapi dan informatif
"""

import logging
import requests
from typing import Optional
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


# ─────────────────────────────────────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────────────────────────────────────

def _escape(text: str) -> str:
    """Escape karakter spesial untuk Telegram MarkdownV2."""
    if text is None:
        return "\\-"
    text = str(text)
    special = r"\_*[]()~`>#+-=|{}.!\\"
    for ch in special:
        text = text.replace(ch, f"\\{ch}")
    return text


def _fmt_price(val) -> str:
    """Format harga IDX dengan pemisah ribuan."""
    if val is None:
        return "\\-"
    try:
        return _escape(f"{float(val):,.0f}")
    except Exception:
        return _escape(str(val))


def _score_bar(score: int) -> str:
    """Buat progress bar visual dari score 0-100."""
    filled = round(score / 10)
    bar = "█" * filled + "░" * (10 - filled)
    return f"{bar} {score}/100"


def _signal_emoji(signal: str) -> str:
    """Emoji sesuai sinyal."""
    return {
        "STRONG_BUY": "🚀",
        "BUY":        "📈",
        "NEUTRAL":    "⚖️",
        "AVOID":      "🚫",
    }.get(signal, "❓")


def _confidence_badge(conf: str) -> str:
    return {"HIGH": "🟢 HIGH", "MEDIUM": "🟡 MEDIUM", "LOW": "🔴 LOW"}.get(conf, conf)


# ─────────────────────────────────────────────────────────────────────────────
# MESSAGE FORMATTER
# ─────────────────────────────────────────────────────────────────────────────

def format_alert_message(tech_data: dict, ai_result: dict) -> str:
    """
    Format pesan alert lengkap dengan data teknikal + analisis AI.
    Menggunakan Telegram MarkdownV2.
    """
    ticker  = ai_result.get("ticker", "UNKNOWN")
    score   = ai_result.get("score", 0)
    signal  = ai_result.get("signal", "NEUTRAL")
    conf    = ai_result.get("confidence", "MEDIUM")
    summary = ai_result.get("summary", "")
    tf      = ai_result.get("timeframe", "-")

    price   = tech_data.get("price", {})
    volume  = tech_data.get("volume", {})
    bo      = tech_data.get("breakout", {})
    sr      = tech_data.get("sr", {})
    rsi     = tech_data.get("rsi", {})
    macd    = tech_data.get("macd", {})
    ema     = tech_data.get("ema", {})
    bb      = tech_data.get("bbands", {})

    entry   = ai_result.get("entry_zone", {})
    rm      = ai_result.get("risk_management", {})
    reasons = ai_result.get("reasoning", {})
    warns   = ai_result.get("warnings", [])
    cats    = ai_result.get("catalysts", [])

    sig_emoji = _signal_emoji(signal)
    close_val = price.get('close')
    change_pct = price.get('change_pct', 0)
    change_arrow = "🔺" if (change_pct or 0) >= 0 else "🔻"

    # ── Header ──────────────────────────────────────────────────────────────
    lines = [
        f"*{_escape('━'*32)}*",
        f"{sig_emoji} *BREAKOUT ALERT \\— {_escape(ticker)}*",
        f"*{_escape('━'*32)}*",
        "",
        f"💰 *Harga:* {_fmt_price(close_val)} {change_arrow} {_escape(str(change_pct))}%",
        f"📅 *Tanggal:* {_escape(price.get('date', '-'))}",
        f"",
        f"🎯 *Sinyal:* `{_escape(signal)}`  {_escape(_confidence_badge(conf))}",
        f"📊 *Score Konfluensi:*",
        f"`{_escape(_score_bar(score))}`",
        "",
        f"💬 *Analisis:*",
        f"_{_escape(summary)}_",
        "",
    ]

    # ── Breakout Detail ──────────────────────────────────────────────────────
    bo_type_label = {
        "resistance_breakout":  "Breakout Resistance",
        "52w_high_breakout":    "Breakout 52W High 🔥",
        "near_breakout":        "Near Breakout ⚠️",
        "none":                 "Tidak breakout",
    }.get(bo.get("breakout_type", "none"), bo.get("breakout_type"))

    lines += [
        f"*{_escape('─'*28)}*",
        f"🚨 *DETAIL BREAKOUT*",
        f"  • Tipe: {_escape(bo_type_label)}",
        f"  • Level: {_fmt_price(bo.get('breakout_level'))}",
        f"  • Volume Ratio: {_escape(str(bo.get('vol_ratio', '-')))}x avg",
        f"  • Volume Surge: {'✅' if bo.get('volume_confirmed') else '❌'}",
        "",
    ]

    # ── Indikator Kunci ──────────────────────────────────────────────────────
    def chk(val): return "✅" if val else "❌"

    lines += [
        f"*{_escape('─'*28)}*",
        f"🔬 *INDIKATOR TEKNIKAL*",
        f"  • RSI\\({14}\\): `{_escape(str(rsi.get('value', '-')))}` — {_escape(rsi.get('zone', '-'))}",
        f"  • MACD Cross: {chk(macd.get('bullish_cross'))} | Hist Growing: {chk(macd.get('histogram_growing'))}",
        f"  • EMA Bullish: {chk(ema.get('bullish_alignment'))} | Above EMA200: {chk(ema.get('price_above_200'))}",
        f"  • BB Squeeze: {chk(bb.get('squeeze'))} | Breakout Upper: {chk(bb.get('price_above_upper'))}",
        "",
    ]

    # ── Level S/R ────────────────────────────────────────────────────────────
    lines += [
        f"*{_escape('─'*28)}*",
        f"📐 *SUPPORT \\& RESISTANCE*",
        f"  • Resistance: {_fmt_price(sr.get('nearest_resistance'))} "
        f"\\({_escape(str(sr.get('dist_resistance_pct', '-')))}%\\)",
        f"  • Support: {_fmt_price(sr.get('nearest_support'))} "
        f"\\({_escape(str(sr.get('dist_support_pct', '-')))}%\\)",
        f"  • 52W High: {_fmt_price(sr.get('high_52w'))}",
        "",
    ]

    # ── Entry & Risk Management ──────────────────────────────────────────────
    rrr = rm.get("risk_reward_ratio", "-")
    lines += [
        f"*{_escape('─'*28)}*",
        f"🎯 *ENTRY \\& MANAJEMEN RISIKO*",
        f"  • Zona Entry: {_fmt_price(entry.get('entry_range_low'))} \\— {_fmt_price(entry.get('entry_range_high'))}",
        f"  • Stop Loss: {_fmt_price(rm.get('stop_loss'))} "
        f"\\({_escape(str(rm.get('stop_loss_pct', '-')))}%\\)",
        f"  • Target 1: {_fmt_price(rm.get('target_1'))} "
        f"\\(\\+{_escape(str(rm.get('target_1_pct', '-')))}%\\)",
        f"  • Target 2: {_fmt_price(rm.get('target_2'))} "
        f"\\(\\+{_escape(str(rm.get('target_2_pct', '-')))}%\\)",
        f"  • Risk/Reward: `{_escape(str(rrr))}:1`",
        f"  • Timeframe: {_escape(tf)}",
        "",
    ]

    # ── Scoring Breakdown ────────────────────────────────────────────────────
    if reasons:
        lines.append(f"*{_escape('─'*28)}*")
        lines.append(f"🔢 *BREAKDOWN SKOR*")
        score_labels = {
            "breakout_price":  "Breakout Level",
            "volume_surge":    "Volume Surge",
            "rsi_momentum":    "RSI Momentum",
            "macd_signal":     "MACD Signal",
            "ema_alignment":   "EMA Alignment",
            "bbands_squeeze":  "BB Squeeze",
            "stoch_mfi":       "Stoch + MFI",
        }
        for key, label in score_labels.items():
            if key in reasons:
                comp = reasons[key]
                s    = comp.get("score", 0)
                note = comp.get("note", "")
                lines.append(f"  • {_escape(label)}: `{_escape(str(s))}` — _{_escape(note[:60])}_")
        lines.append("")

    # ── Catalysts ────────────────────────────────────────────────────────────
    if cats:
        lines.append(f"✨ *FAKTOR POSITIF*")
        for cat in cats[:3]:
            lines.append(f"  \\+ {_escape(cat)}")
        lines.append("")

    # ── Warnings ─────────────────────────────────────────────────────────────
    if warns:
        lines.append(f"⚠️ *PERINGATAN*")
        for w in warns[:3]:
            lines.append(f"  \\! {_escape(w)}")
        lines.append("")

    # ── Footer ───────────────────────────────────────────────────────────────
    lines += [
        f"*{_escape('─'*28)}*",
        f"🤖 _Analisis oleh Stock Bot IDX \\| Powered by Claude AI_",
        f"⚠️ _Bukan rekomendasi investasi\\. DYOR\\!_",
    ]

    return "\n".join(lines)


def format_summary_message(results: list) -> str:
    """Format pesan ringkasan untuk semua saham yang dianalisa hari ini."""
    total   = len(results)
    alerts  = [r for r in results if r.get("alert_sent")]
    skipped = total - len(alerts)

    lines = [
        f"*{_escape('═'*32)}*",
        f"📋 *LAPORAN SCAN EOD*",
        f"*{_escape('═'*32)}*",
        f"",
        f"📊 Total dipindai: *{total}* saham",
        f"🚀 Alert dikirim: *{len(alerts)}* saham",
        f"⏭️ Di-skip: *{skipped}* saham",
        f"",
    ]

    if alerts:
        lines.append("*Saham yang masuk kriteria:*")
        for r in sorted(alerts, key=lambda x: x.get("score", 0), reverse=True):
            t = _escape(r.get("ticker", ""))
            s = _escape(str(r.get("score", 0)))
            sig = _escape(r.get("signal", ""))
            lines.append(f"  • *{t}* \\— Score: `{s}` \\— {sig}")
        lines.append("")

    lines += [
        f"_Scan berikutnya: besok setelah penutupan IDX_",
        f"*{_escape('─'*28)}*",
    ]

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# SENDER
# ─────────────────────────────────────────────────────────────────────────────

def send_message(text: str, chat_id: str = None, parse_mode: str = "MarkdownV2") -> bool:
    """Kirim pesan teks ke Telegram."""
    cid = chat_id or TELEGRAM_CHAT_ID
    if not cid or not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN atau TELEGRAM_CHAT_ID belum dikonfigurasi")
        return False

    try:
        resp = requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id":    cid,
                "text":       text,
                "parse_mode": parse_mode,
                "disable_web_page_preview": True,
            },
            timeout=15,
        )
        data = resp.json()
        if data.get("ok"):
            logger.info(f"Telegram: Pesan terkirim (chat_id={cid})")
            return True
        else:
            logger.error(f"Telegram API error: {data.get('description')}")
            # Fallback: kirim tanpa formatting jika error parsing
            if "can't parse" in str(data.get("description", "")):
                return send_plain_fallback(text, cid)
            return False
    except Exception as e:
        logger.error(f"Gagal kirim Telegram: {e}")
        return False


def send_plain_fallback(text: str, chat_id: str) -> bool:
    """Kirim sebagai plain text jika MarkdownV2 gagal."""
    import re
    clean = re.sub(r"[_*\[\]()~`>#+=|{}.!\\]", "", text)
    try:
        resp = requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={"chat_id": chat_id, "text": clean[:4096]},
            timeout=15,
        )
        return resp.json().get("ok", False)
    except Exception:
        return False


def send_alert(tech_data: dict, ai_result: dict) -> bool:
    """Kirim alert lengkap breakout ke Telegram."""
    try:
        message = format_alert_message(tech_data, ai_result)
        # Telegram max 4096 karakter per pesan
        if len(message) > 4000:
            message = message[:3900] + "\n\n_\\.\\.\\. pesan dipotong_"
        return send_message(message)
    except Exception as e:
        logger.error(f"Error send_alert: {e}", exc_info=True)
        return False


def send_startup_message() -> None:
    """Kirim pesan ketika bot pertama kali dijalankan."""
    msg = (
        "🤖 *Stock Breakout Bot IDX* sudah berjalan\\!\n\n"
        "📅 Scan akan dilakukan setiap hari setelah penutupan IDX\\.\n"
        "💬 Ketik /status untuk cek status bot\\."
    )
    send_message(msg)


def send_error_notification(error_msg: str) -> None:
    """Kirim notifikasi error ke Telegram."""
    msg = f"⚠️ *BOT ERROR*\n\n`{_escape(error_msg[:500])}`"
    send_message(msg)
