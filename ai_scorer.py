"""
ai_scorer.py — Groq AI scoring untuk Stock Bot IDX
"""

import json
import logging
import os
import re
import time
from typing import Optional

from groq import Groq

from config import SCORE_WEIGHTS, MIN_SCORE

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b").strip()

if not GROQ_API_KEY:
    logger.warning("GROQ_API_KEY belum di-set.")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

_rate_limited_until = 0.0


def build_analysis_prompt(data: dict) -> str:
    ticker = data.get("ticker", "UNKNOWN")
    price = data.get("price", {})
    ema = data.get("ema", {})
    rsi = data.get("rsi", {})
    macd = data.get("macd", {})
    bb = data.get("bbands", {})
    stoch = data.get("stochastic", {})
    mfi = data.get("mfi", {})
    obv = data.get("obv", {})
    vwap = data.get("vwap", {})
    volume = data.get("volume", {})
    sr = data.get("sr", {})
    bo = data.get("breakout", {})
    atr = data.get("atr", {})

    return f"""
Kamu adalah analis teknikal saham senior spesialis pasar IDX Indonesia.

Jawab HANYA dengan JSON valid.
Jangan gunakan markdown atau teks di luar JSON.

DATA SAHAM {ticker}

HARGA:
Close={price.get('close')}
Open={price.get('open')}
High={price.get('high')}
Low={price.get('low')}
Perubahan={price.get('change_pct')}%

BREAKOUT:
is_breakout={bo.get('is_breakout')}
tipe={bo.get('breakout_type')}
level={bo.get('breakout_level')}
jarak={bo.get('breakout_pct')}%

VOLUME:
hari_ini={volume.get('today')}
avg_20d={volume.get('avg_20d')}
ratio={volume.get('ratio')}x
surge={volume.get('surge')}

SUPPORT / RESISTANCE:
resistance={sr.get('nearest_resistance')}
support={sr.get('nearest_support')}
high_52w={sr.get('high_52w')}
low_52w={sr.get('low_52w')}

EMA:
EMA9={ema.get('ema9')}
EMA21={ema.get('ema21')}
EMA50={ema.get('ema50')}
EMA200={ema.get('ema200')}
bullish_alignment={ema.get('bullish_alignment')}
above_ema200={ema.get('price_above_200')}

RSI:
value={rsi.get('value')}
zone={rsi.get('zone')}
direction={rsi.get('direction')}

MACD:
macd={macd.get('macd')}
signal={macd.get('signal')}
histogram={macd.get('histogram')}
bullish_cross={macd.get('bullish_cross')}
hist_growing={macd.get('histogram_growing')}

BOLLINGER BANDS:
upper={bb.get('upper')}
mid={bb.get('mid')}
lower={bb.get('lower')}
squeeze={bb.get('squeeze')}
breakout_upper={bb.get('price_above_upper')}

STOCHASTIC:
K={stoch.get('k')}
D={stoch.get('d')}
bullish_cross={stoch.get('bullish_cross')}

MFI:
value={mfi.get('value')}
zone={mfi.get('zone')}

OBV:
above_ema={obv.get('above_ema')}
rising={obv.get('rising')}

VWAP:
value={vwap.get('value_20d')}
price_above={vwap.get('price_above')}

ATR:
value={atr.get('value')}
pct={atr.get('pct_of_price')}%

Berikan JSON dengan struktur berikut:

{{
    "ticker": "{ticker}",
    "score": 0,
    "signal": "NEUTRAL",
    "confidence": "MEDIUM",
    "summary": "Ringkasan analisis dalam Bahasa Indonesia.",

    "reasoning": {{

        "breakout_price": {{
            "score": 0,
            "note": "Analisis breakout"
        }},

        "volume_surge": {{
            "score": 0,
            "note": "Analisis volume"
        }},

        "rsi_momentum": {{
            "score": 0,
            "note": "Analisis RSI"
        }},

        "macd_signal": {{
            "score": 0,
            "note": "Analisis MACD"
        }},

        "ema_alignment": {{
            "score": 0,
            "note": "Analisis EMA"
        }},

        "bbands_squeeze": {{
            "score": 0,
            "note": "Analisis Bollinger"
        }},

        "stoch_mfi": {{
            "score": 0,
            "note": "Analisis Stochastic dan MFI"
        }}
    }},

    "entry_zone": {{
        "ideal_entry": 0,
        "entry_range_low": 0,
        "entry_range_high": 0
    }},

    "risk_management": {{
        "stop_loss": 0,
        "stop_loss_pct": 0,
        "target_1": 0,
        "target_1_pct": 0,
        "target_2": 0,
        "target_2_pct": 0,
        "risk_reward_ratio": 0
    }},

    "warnings": [],
    "catalysts": [],
    "timeframe": "3-7 hari"
}}

ATURAN SCORE:

STRONG_BUY = score >= 80
BUY = score 65-79
NEUTRAL = score 45-64
AVOID = score < 45

Pertimbangkan breakout, volume, RSI, MACD, EMA,
Bollinger Bands, Stochastic, MFI, OBV, VWAP,
support/resistance dan ATR.

Volume konfirmasi sangat penting untuk breakout IDX.

Stop loss harus mempertimbangkan ATR dan support.

Jangan membuat data fundamental yang tidak diberikan.
""".strip()


def _send_reply(chat_id, reply_fn, text):
    if chat_id and reply_fn:
        try:
            reply_fn(chat_id, text)
        except Exception as e:
            logger.error(
                "Gagal mengirim pesan error Telegram: %s",
                e
            )


def _get_retry_after(exc) -> Optional[float]:

    response = getattr(exc, "response", None)
    headers = getattr(response, "headers", None)

    if headers:

        value = (
            headers.get("retry-after")
            or headers.get("Retry-After")
        )

        if value:

            try:
                return max(
                    1.0,
                    float(value)
                )

            except (TypeError, ValueError):
                pass

    text = str(exc)

    match = re.search(
        r"retry[- ]after[\"':=\s]+([0-9]+(?:\.[0-9]+)?)",
        text,
        re.I
    )

    if match:
        return max(
            1.0,
            float(match.group(1))
        )

    return None


def _is_rate_limit_error(exc):

    status = getattr(
        exc,
        "status_code",
        None
    )

    if status == 429:
        return True

    text = str(exc).lower()

    return (
        "429" in text
        or "rate limit" in text
        or "too many requests" in text
    )


def _is_temporary_error(exc):

    status = getattr(
        exc,
        "status_code",
        None
    )

    if status in (
        408,
        409,
        429,
        500,
        502,
        503,
        504
    ):
        return True

    text = str(exc).lower()

    return any(
        x in text
        for x in [
            "timeout",
            "timed out",
            "connection",
            "temporarily unavailable",
            "server error",
            "service unavailable"
        ]
    )


def _clean_json_text(raw_text: str) -> str:

    text = (
        raw_text or ""
    ).strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.I
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    ).strip()

    start = text.find("{")
    end = text.rfind("}")

    if start >= 0 and end > start:
        text = text[
            start:end + 1
        ]

    return text.strip()


def analyze_with_ai(
    data: dict,
    _chat_id=None,
    _reply_fn=None
) -> Optional[dict]:

    global _rate_limited_until

    ticker = data.get(
        "ticker",
        "UNKNOWN"
    )

    if client is None:

        logger.error(
            "[%s] GROQ_API_KEY kosong.",
            ticker
        )

        _send_reply(
            _chat_id,
            _reply_fn,
            "❌ <b>Groq API Key belum tersedia.</b>\n\n"
            "Pastikan environment variable "
            "<code>GROQ_API_KEY</code> "
            "sudah diisi di Railway."
        )

        return None

    now = time.time()

    if now < _rate_limited_until:

        sisa = max(
            1,
            int(
                _rate_limited_until - now
            )
        )

        menit, detik = divmod(
            sisa,
            60
        )

        waktu = (
            f"{menit}m {detik}s"
            if menit
            else f"{detik}s"
        )

        logger.warning(
            "[%s] Rate-limit cooldown aktif: %s",
            ticker,
            waktu
        )

        _send_reply(
            _chat_id,
            _reply_fn,
            "⚠️ <b>Groq sedang rate limit.</b>\n\n"
            f"Coba lagi dalam sekitar "
            f"<b>{waktu}</b>."
        )

        return None

    prompt = build_analysis_prompt(
        data
    )

    raw_text = ""

    max_attempts = 3

    for attempt in range(
        1,
        max_attempts + 1
    ):

        try:

response = client.chat.completions.create(
    model=GROQ_MODEL,

    messages=[
        {
            "role": "system",
            "content": (
                "Kamu adalah analis teknikal saham IDX profesional. "
                "Analisis data teknikal yang diberikan. "
                "Jawab HANYA dalam JSON valid. "
                "Jangan memberikan teks di luar JSON."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ],

    # GPT-OSS adalah reasoning model.
    # LOW membuat reasoning tidak menghabiskan
    # seluruh token sebelum menghasilkan jawaban.
    reasoning_effort="low",

    # Paksa output menjadi JSON.
    response_format={
        "type": "json_object"
    },

    # Jangan terlalu tinggi supaya cepat.
    temperature=0.1,

    # Beri ruang untuk reasoning + JSON.
    max_completion_tokens=3000
)
            raw_text = (
                response
                .choices[0]
                .message
                .content
                or ""
            )
if not raw_text.strip():

    logger.error(
        "[%s] Groq mengembalikan content kosong.",
        ticker
    )

    message = response.choices[0].message

    logger.error(
        "[%s] Response message: %s",
        ticker,
        message
    )

    _send_reply(
        _chat_id,
        _reply_fn,
        "⚠️ <b>AI tidak menghasilkan teks jawaban.</b>\n"
        "Bot akan mencoba lagi pada request berikutnya."
    )

    return None

            cleaned = _clean_json_text(
                raw_text
            )

            result = json.loads(
                cleaned
            )

            if not isinstance(
                result,
                dict
            ):
                raise ValueError(
                    "Response AI bukan JSON object."
                )

            result["ticker"] = ticker

            score = result.get(
                "score"
            )

            signal = result.get(
                "signal"
            )

            if score is not None:

                try:

                    result["score"] = max(
                        0,
                        min(
                            100,
                            int(
                                float(score)
                            )
                        )
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    result["score"] = 0

            if signal not in (
                "STRONG_BUY",
                "BUY",
                "NEUTRAL",
                "AVOID"
            ):

                result["signal"] = (
                    "NEUTRAL"
                )

            _rate_limited_until = 0.0

            logger.info(
                "[%s] Groq Score: %s/100 — %s | model=%s",
                ticker,
                result.get("score"),
                result.get("signal"),
                GROQ_MODEL
            )

            return result

        except json.JSONDecodeError as e:

            logger.error(
                "[%s] Gagal parse JSON AI: %s | Raw: %s",
                ticker,
                e,
                raw_text[:500]
            )

            _send_reply(
                _chat_id,
                _reply_fn,
                "⚠️ <b>AI mengirim format hasil "
                "yang tidak valid.</b>\n"
                "Coba perintah tersebut sekali lagi."
            )

            return None

        except Exception as e:

            status = getattr(
                e,
                "status_code",
                None
            )

            logger.error(
                "[%s] Groq error attempt %s/%s | "
                "status=%s | %s",
                ticker,
                attempt,
                max_attempts,
                status,
                e
            )

            # RATE LIMIT
            if _is_rate_limit_error(e):

                retry_after = (
                    _get_retry_after(e)
                )

                if retry_after is None:

                    retry_after = min(
                        60.0,
                        2 ** attempt
                    )

                _rate_limited_until = (
                    time.time()
                    + retry_after
                )

                logger.warning(
                    "[%s] RATE LIMIT 429. "
                    "retry-after=%ss",
                    ticker,
                    retry_after
                )

                if (
                    attempt < max_attempts
                    and retry_after <= 30
                ):

                    time.sleep(
                        retry_after
                    )

                    continue

                if retry_after >= 60:

                    waktu = (
                        f"{int(retry_after // 60)}m "
                        f"{int(retry_after % 60)}s"
                    )

                else:

                    waktu = (
                        f"{int(retry_after)} detik"
                    )

                _send_reply(
                    _chat_id,
                    _reply_fn,
                    "⚠️ <b>Groq API sedang "
                    "rate limit.</b>\n\n"
                    f"Groq meminta menunggu "
                    f"sekitar <b>{waktu}</b> "
                    "sebelum request berikutnya."
                )

                return None

            # API KEY
            if (
                status == 401
                or "authentication"
                in str(e).lower()
                or "invalid api key"
                in str(e).lower()
            ):

                _send_reply(
                    _chat_id,
                    _reply_fn,
                    "❌ <b>Groq API Key bermasalah.</b>\n\n"
                    "Periksa "
                    "<code>GROQ_API_KEY</code> "
                    "di Railway → Variables."
                )

                return None

            # MODEL
            if (
                status == 404
                or (
                    "model"
                    in str(e).lower()
                    and "not found"
                    in str(e).lower()
                )
            ):

                _send_reply(
                    _chat_id,
                    _reply_fn,
                    "❌ <b>Model Groq tidak ditemukan.</b>\n\n"
                    f"Model saat ini: "
                    f"<code>{GROQ_MODEL}</code>"
                )

                return None

            # TEMPORARY ERROR
            if (
                _is_temporary_error(e)
                and attempt < max_attempts
            ):

                delay = min(
                    8.0,
                    2 ** (attempt - 1)
                )

                logger.warning(
                    "[%s] Temporary error, "
                    "retry %ss...",
                    ticker,
                    delay
                )

                time.sleep(
                    delay
                )

                continue

            _send_reply(
                _chat_id,
                _reply_fn,
                "❌ <b>Groq gagal memproses analisis.</b>\n\n"
                f"Status: "
                f"<code>{status or 'unknown'}</code>\n"
                "Cek log Railway untuk detail error."
            )

            return None

    return None


def should_send_alert(
    ai_result: dict
) -> bool:

    if not ai_result:
        return False

    score = ai_result.get(
        "score",
        0
    )

    signal = ai_result.get(
        "signal",
        "NEUTRAL"
    )

    return (
        score >= MIN_SCORE
        and signal in (
            "STRONG_BUY",
            "BUY"
        )
    )
