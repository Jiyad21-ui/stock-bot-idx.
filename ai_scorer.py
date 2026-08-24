"""
ai_scorer.py
AI Technical Analysis menggunakan Groq
Stock Bot IDX
"""

import json
import logging
import os
import re
import time
from typing import Optional

from groq import Groq

from config import SCORE_WEIGHTS, MIN_SCORE


# ============================================================
# LOGGER
# ============================================================

logger = logging.getLogger(__name__)


# ============================================================
# GROQ CONFIGURATION
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
).strip()


if not GROQ_API_KEY:

    logger.warning(
        "GROQ_API_KEY belum di-set."
    )


client = (
    Groq(
        api_key=GROQ_API_KEY
    )
    if GROQ_API_KEY
    else None
)


# ============================================================
# RATE LIMIT STATE
# ============================================================

_rate_limited_until = 0.0


# ============================================================
# BUILD PROMPT
# ============================================================

def build_analysis_prompt(data: dict) -> str:

    ticker = data.get(
        "ticker",
        "UNKNOWN"
    )

    price = data.get(
        "price",
        {}
    )

    ema = data.get(
        "ema",
        {}
    )

    rsi = data.get(
        "rsi",
        {}
    )

    macd = data.get(
        "macd",
        {}
    )

    bb = data.get(
        "bbands",
        {}
    )

    stoch = data.get(
        "stochastic",
        {}
    )

    mfi = data.get(
        "mfi",
        {}
    )

    obv = data.get(
        "obv",
        {}
    )

    vwap = data.get(
        "vwap",
        {}
    )

    volume = data.get(
        "volume",
        {}
    )

    sr = data.get(
        "sr",
        {}
    )

    breakout = data.get(
        "breakout",
        {}
    )

    atr = data.get(
        "atr",
        {}
    )


    prompt = f"""
Kamu adalah analis teknikal saham profesional
yang fokus pada saham Bursa Efek Indonesia (IDX).

Analisis data teknikal yang diberikan.

PENTING:

1. Jangan mengarang data.
2. Gunakan hanya data yang diberikan.
3. Jangan membuat berita atau fundamental yang tidak diberikan.
4. Pertimbangkan risiko.
5. Volume sangat penting untuk validasi breakout.
6. Gunakan Bahasa Indonesia.
7. Jawaban WAJIB berupa JSON valid.
8. Jangan menggunakan markdown.
9. Jangan menggunakan ```json.
10. Jangan menambahkan teks sebelum atau sesudah JSON.

==================================================
SAHAM
==================================================

Ticker:
{ticker}

==================================================
HARGA
==================================================

Close:
{price.get('close')}

Open:
{price.get('open')}

High:
{price.get('high')}

Low:
{price.get('low')}

Perubahan:
{price.get('change_pct')}%

==================================================
BREAKOUT
==================================================

Breakout:
{breakout.get('is_breakout')}

Breakout Type:
{breakout.get('breakout_type')}

Breakout Level:
{breakout.get('breakout_level')}

Breakout Distance:
{breakout.get('breakout_pct')}%

==================================================
VOLUME
==================================================

Volume Hari Ini:
{volume.get('today')}

Average Volume 20 Hari:
{volume.get('avg_20d')}

Volume Ratio:
{volume.get('ratio')}x

Volume Surge:
{volume.get('surge')}

==================================================
SUPPORT RESISTANCE
==================================================

Nearest Resistance:
{sr.get('nearest_resistance')}

Nearest Support:
{sr.get('nearest_support')}

52 Week High:
{sr.get('high_52w')}

52 Week Low:
{sr.get('low_52w')}

==================================================
EMA
==================================================

EMA9:
{ema.get('ema9')}

EMA21:
{ema.get('ema21')}

EMA50:
{ema.get('ema50')}

EMA200:
{ema.get('ema200')}

Bullish Alignment:
{ema.get('bullish_alignment')}

Price Above EMA200:
{ema.get('price_above_200')}

==================================================
RSI
==================================================

RSI:
{rsi.get('value')}

RSI Zone:
{rsi.get('zone')}

RSI Direction:
{rsi.get('direction')}

==================================================
MACD
==================================================

MACD:
{macd.get('macd')}

Signal:
{macd.get('signal')}

Histogram:
{macd.get('histogram')}

Bullish Cross:
{macd.get('bullish_cross')}

Histogram Growing:
{macd.get('histogram_growing')}

==================================================
BOLLINGER BANDS
==================================================

Upper:
{bb.get('upper')}

Middle:
{bb.get('mid')}

Lower:
{bb.get('lower')}

Squeeze:
{bb.get('squeeze')}

Price Above Upper:
{bb.get('price_above_upper')}

==================================================
STOCHASTIC
==================================================

K:
{stoch.get('k')}

D:
{stoch.get('d')}

Bullish Cross:
{stoch.get('bullish_cross')}

==================================================
MFI
==================================================

MFI:
{mfi.get('value')}

MFI Zone:
{mfi.get('zone')}

==================================================
OBV
==================================================

Above EMA:
{obv.get('above_ema')}

Rising:
{obv.get('rising')}

==================================================
VWAP
==================================================

VWAP 20D:
{vwap.get('value_20d')}

Price Above VWAP:
{vwap.get('price_above')}

==================================================
ATR
==================================================

ATR:
{atr.get('value')}

ATR Percentage:
{atr.get('pct_of_price')}%

==================================================
SCORING
==================================================

Berikan score 0 sampai 100.

Interpretasi:

80 - 100
STRONG_BUY

65 - 79
BUY

45 - 64
NEUTRAL

0 - 44
AVOID

==================================================
OUTPUT JSON
==================================================

Kembalikan JSON dengan struktur PERSIS seperti berikut:

{{
    "ticker": "{ticker}",

    "score": 0,

    "signal": "NEUTRAL",

    "confidence": "MEDIUM",

    "summary": "Ringkasan analisis saham dalam Bahasa Indonesia.",

    "reasoning": {{

        "breakout_price": {{
            "score": 0,
            "note": "Analisis breakout."
        }},

        "volume_surge": {{
            "score": 0,
            "note": "Analisis volume."
        }},

        "rsi_momentum": {{
            "score": 0,
            "note": "Analisis RSI."
        }},

        "macd_signal": {{
            "score": 0,
            "note": "Analisis MACD."
        }},

        "ema_alignment": {{
            "score": 0,
            "note": "Analisis EMA."
        }},

        "bbands_squeeze": {{
            "score": 0,
            "note": "Analisis Bollinger Bands."
        }},

        "stoch_mfi": {{
            "score": 0,
            "note": "Analisis Stochastic dan MFI."
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

==================================================
ATURAN ANALISIS
==================================================

Score tinggi jika:

- Breakout valid
- Volume meningkat
- Harga di atas EMA penting
- EMA bullish alignment
- RSI mendukung momentum
- MACD bullish
- Histogram MACD meningkat
- Bollinger breakout
- Stochastic bullish
- MFI sehat
- OBV meningkat
- Harga di atas VWAP

Kurangi score jika:

- Tidak ada breakout
- Volume rendah
- Harga di bawah EMA200
- RSI lemah
- MACD bearish
- Volume tidak mengkonfirmasi breakout
- Resistance sangat dekat
- Risiko terlalu tinggi

Stop loss harus mempertimbangkan:

- Support terdekat
- ATR
- Volatilitas saham

Target harus realistis berdasarkan:

- Resistance
- ATR
- Risk reward

Jangan memberikan kepastian keuntungan.

==================================================
"""

    return prompt.strip()


# ============================================================
# SEND TELEGRAM MESSAGE
# ============================================================

def _send_reply(
    chat_id,
    reply_fn,
    text
):

    if not chat_id:
        return

    if not reply_fn:
        return

    try:

        reply_fn(
            chat_id,
            text
        )

    except Exception as e:

        logger.error(
            "Gagal mengirim pesan Telegram: %s",
            e
        )


# ============================================================
# GET RETRY AFTER
# ============================================================

def _get_retry_after(
    exc
) -> Optional[float]:

    response = getattr(
        exc,
        "response",
        None
    )

    headers = getattr(
        response,
        "headers",
        None
    )


    if headers:

        value = (
            headers.get(
                "retry-after"
            )
            or
            headers.get(
                "Retry-After"
            )
        )

        if value:

            try:

                return max(
                    1.0,
                    float(value)
                )

            except (
                TypeError,
                ValueError
            ):

                pass


    text = str(
        exc
    )


    match = re.search(
        r"retry[- ]after[\"':=\s]+([0-9]+(?:\.[0-9]+)?)",
        text,
        re.IGNORECASE
    )


    if match:

        return max(
            1.0,
            float(
                match.group(1)
            )
        )


    return None


# ============================================================
# CHECK RATE LIMIT
# ============================================================

def _is_rate_limit_error(
    exc
):

    status = getattr(
        exc,
        "status_code",
        None
    )


    if status == 429:

        return True


    text = str(
        exc
    ).lower()


    return (
        "429" in text
        or
        "rate limit" in text
        or
        "too many requests" in text
    )


# ============================================================
# CHECK TEMPORARY ERROR
# ============================================================

def _is_temporary_error(
    exc
):

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


    text = str(
        exc
    ).lower()


    temporary_words = [

        "timeout",

        "timed out",

        "connection",

        "temporarily unavailable",

        "server error",

        "service unavailable"

    ]


    return any(
        word in text
        for word in temporary_words
    )


# ============================================================
# CLEAN JSON
# ============================================================

def _clean_json_text(
    raw_text: str
) -> str:

    text = (
        raw_text or ""
    ).strip()


    # Remove markdown JSON fence

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )


    text = re.sub(
        r"\s*```$",
        "",
        text
    )


    text = text.strip()


    # Cari object JSON

    start = text.find(
        "{"
    )

    end = text.rfind(
        "}"
    )


    if (
        start >= 0
        and
        end > start
    ):

        text = text[
            start:end + 1
        ]


    return text.strip()


# ============================================================
# MAIN AI ANALYSIS
# ============================================================

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


    # ========================================================
    # CHECK API KEY
    # ========================================================

    if client is None:

        logger.error(
            "[%s] GROQ_API_KEY kosong.",
            ticker
        )


        _send_reply(
            _chat_id,
            _reply_fn,

            "❌ <b>Groq API Key belum tersedia.</b>\n\n"
            "Pastikan variable "
            "<code>GROQ_API_KEY</code> "
            "sudah diisi di Railway."
        )


        return None


    # ========================================================
    # CHECK RATE LIMIT COOLDOWN
    # ========================================================

    now = time.time()


    if now < _rate_limited_until:

        remaining = max(
            1,
            int(
                _rate_limited_until
                - now
            )
        )


        minutes, seconds = divmod(
            remaining,
            60
        )


        if minutes:

            wait_text = (
                f"{minutes}m "
                f"{seconds}s"
            )

        else:

            wait_text = (
                f"{seconds}s"
            )


        logger.warning(
            "[%s] Rate-limit cooldown aktif: %s",
            ticker,
            wait_text
        )


        _send_reply(
            _chat_id,
            _reply_fn,

            "⚠️ <b>Groq sedang rate limit.</b>\n\n"
            f"Coba lagi dalam sekitar "
            f"<b>{wait_text}</b>."
        )


        return None


    # ========================================================
    # BUILD PROMPT
    # ========================================================

    prompt = build_analysis_prompt(
        data
    )


    raw_text = ""


    # ========================================================
    # RETRY
    # ========================================================

    max_attempts = 3


    for attempt in range(
        1,
        max_attempts + 1
    ):

        try:

            # =================================================
            # GROQ REQUEST
            # =================================================

            response = client.chat.completions.create(

                model=GROQ_MODEL,

                messages=[

                    {
                        "role": "system",

                        "content": (
                            "Kamu adalah analis "
                            "teknikal saham IDX "
                            "profesional. "

                            "Analisis data "
                            "teknikal yang "
                            "diberikan. "

                            "Jawab HANYA "
                            "dalam JSON valid. "

                            "Jangan memberikan "
                            "teks di luar JSON."
                        )
                    },

                    {
                        "role": "user",

                        "content": prompt
                    }

                ],

                # GPT-OSS reasoning
                reasoning_effort="low",

                # Paksa JSON
                response_format={
                    "type": "json_object"
                },

                temperature=0.1,

                # Ruang reasoning + output
                max_completion_tokens=3000
            )


            # =================================================
            # GET RESPONSE
            # =================================================

            raw_text = (

                response
                .choices[0]
                .message
                .content

                or ""

            )


            # =================================================
            # CHECK EMPTY RESPONSE
            # =================================================

            if not raw_text.strip():

                logger.error(
                    "[%s] Groq mengembalikan "
                    "content kosong.",
                    ticker
                )


                message = (
                    response
                    .choices[0]
                    .message
                )


                logger.error(
                    "[%s] Response message: %s",
                    ticker,
                    message
                )


                _send_reply(
                    _chat_id,
                    _reply_fn,

                    "⚠️ <b>AI tidak menghasilkan "
                    "teks jawaban.</b>\n\n"
                    "Coba perintah tersebut "
                    "sekali lagi."
                )


                return None


            # =================================================
            # CLEAN RESPONSE
            # =================================================

            cleaned = _clean_json_text(
                raw_text
            )


            # =================================================
            # PARSE JSON
            # =================================================

            result = json.loads(
                cleaned
            )


            # =================================================
            # VALIDATE OBJECT
            # =================================================

            if not isinstance(
                result,
                dict
            ):

                raise ValueError(
                    "Response AI bukan "
                    "JSON object."
                )


            # =================================================
            # FORCE TICKER
            # =================================================

            result["ticker"] = (
                ticker
            )


            # =================================================
            # SCORE
            # =================================================

            score = result.get(
                "score"
            )


            if score is not None:

                try:

                    result["score"] = max(

                        0,

                        min(

                            100,

                            int(
                                float(
                                    score
                                )
                            )

                        )

                    )

                except (
                    TypeError,
                    ValueError
                ):

                    result["score"] = 0

            else:

                result["score"] = 0


            # =================================================
            # SIGNAL
            # =================================================

            signal = result.get(
                "signal"
            )


            allowed_signals = (

                "STRONG_BUY",

                "BUY",

                "NEUTRAL",

                "AVOID"

            )


            if signal not in allowed_signals:

                result["signal"] = (
                    "NEUTRAL"
                )


            # =================================================
            # CONFIDENCE
            # =================================================

            confidence = result.get(
                "confidence"
            )


            if confidence not in (
                "HIGH",
                "MEDIUM",
                "LOW"
            ):

                result["confidence"] = (
                    "MEDIUM"
                )


            # =================================================
            # SUCCESS
            # =================================================

            _rate_limited_until = 0.0


            logger.info(

                "[%s] Groq Score: %s/100 | "
                "Signal: %s | "
                "Confidence: %s | "
                "Model: %s",

                ticker,

                result.get(
                    "score"
                ),

                result.get(
                    "signal"
                ),

                result.get(
                    "confidence"
                ),

                GROQ_MODEL

            )


            return result


        # ====================================================
        # JSON ERROR
        # ====================================================

        except json.JSONDecodeError as e:

            logger.error(

                "[%s] Gagal parse JSON AI: %s | Raw: %s",

                ticker,

                e,

                raw_text[:2000]

            )


            _send_reply(

                _chat_id,

                _reply_fn,

                "⚠️ <b>AI mengirim format "
                "hasil yang tidak valid.</b>\n\n"
                "Coba perintah tersebut "
                "sekali lagi."

            )


            return None


        # ====================================================
        # GENERAL ERROR
        # ====================================================

        except Exception as e:

            status = getattr(

                e,

                "status_code",

                None

            )


            logger.error(

                "[%s] Groq error "
                "attempt %s/%s | "
                "status=%s | %s",

                ticker,

                attempt,

                max_attempts,

                status,

                e

            )


            # ================================================
            # RATE LIMIT 429
            # ================================================

            if _is_rate_limit_error(
                e
            ):

                retry_after = (
                    _get_retry_after(
                        e
                    )
                )


                if retry_after is None:

                    retry_after = min(

                        60.0,

                        2 ** attempt

                    )


                _rate_limited_until = (

                    time.time()
                    +
                    retry_after

                )


                logger.warning(

                    "[%s] RATE LIMIT 429 | "
                    "retry-after=%ss",

                    ticker,

                    retry_after

                )


                # Retry jika waktunya pendek

                if (

                    attempt < max_attempts

                    and

                    retry_after <= 30

                ):

                    time.sleep(
                        retry_after
                    )

                    continue


                # Inform Telegram

                if retry_after >= 60:

                    minutes = int(
                        retry_after // 60
                    )

                    seconds = int(
                        retry_after % 60
                    )

                    wait_text = (
                        f"{minutes}m "
                        f"{seconds}s"
                    )

                else:

                    wait_text = (
                        f"{int(retry_after)} detik"
                    )


                _send_reply(

                    _chat_id,

                    _reply_fn,

                    "⚠️ <b>Groq API sedang "
                    "rate limit.</b>\n\n"

                    f"Groq meminta menunggu "
                    f"sekitar <b>{wait_text}</b> "
                    "sebelum request berikutnya."

                )


                return None


            # ================================================
            # INVALID API KEY
            # ================================================

            error_text = str(
                e
            ).lower()


            if (

                status == 401

                or

                "authentication"
                in error_text

                or

                "invalid api key"
                in error_text

            ):

                _send_reply(

                    _chat_id,

                    _reply_fn,

                    "❌ <b>Groq API Key "
                    "bermasalah.</b>\n\n"

                    "Periksa variable "
                    "<code>GROQ_API_KEY</code> "
                    "di Railway."

                )


                return None


            # ================================================
            # MODEL NOT FOUND
            # ================================================

            if (

                status == 404

                or (

                    "model"
                    in error_text

                    and

                    "not found"
                    in error_text

                )

            ):

                _send_reply(

                    _chat_id,

                    _reply_fn,

                    "❌ <b>Model Groq "
                    "tidak ditemukan.</b>\n\n"

                    f"Model saat ini: "
                    f"<code>{GROQ_MODEL}</code>"

                )


                return None


            # ================================================
            # TEMPORARY ERROR
            # ================================================

            if (

                _is_temporary_error(
                    e
                )

                and

                attempt < max_attempts

            ):

                delay = min(

                    8.0,

                    2 ** (
                        attempt - 1
                    )

                )


                logger.warning(

                    "[%s] Temporary error. "
                    "Retry dalam %ss...",

                    ticker,

                    delay

                )


                time.sleep(
                    delay
                )


                continue


            # ================================================
            # OTHER ERROR
            # ================================================

            _send_reply(

                _chat_id,

                _reply_fn,

                "❌ <b>Groq gagal "
                "memproses analisis.</b>\n\n"

                f"Status: "
                f"<code>{status or 'unknown'}</code>\n\n"

                "Cek log Railway untuk "
                "detail error."

            )


            return None


    return None


# ============================================================
# ALERT FILTER
# ============================================================

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

        and

        signal in (

            "STRONG_BUY",

            "BUY"

        )

    )
