"""
ai_scorer.py — Pakai Groq AI (GRATIS) untuk scoring multi-indikator
"""

import json
import logging
import os
from groq import Groq
from typing import Optional
from config import SCORE_WEIGHTS, MIN_SCORE

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
client = Groq(api_key=GROQ_API_KEY)


def build_analysis_prompt(data: dict) -> str:
    ticker  = data.get("ticker", "UNKNOWN")
    price   = data.get("price", {})
    ema     = data.get("ema", {})
    rsi     = data.get("rsi", {})
    macd    = data.get("macd", {})
    bb      = data.get("bbands", {})
    stoch   = data.get("stochastic", {})
    mfi     = data.get("mfi", {})
    obv     = data.get("obv", {})
    vwap    = data.get("vwap", {})
    volume  = data.get("volume", {})
    sr      = data.get("sr", {})
    bo      = data.get("breakout", {})
    atr     = data.get("atr", {})

    prompt = fa
Kamu adalah analis teknikal saham senior spesialis pasar IDX Indonesia.
Jawab HANYA dengan JSON valid, tanpa teks apapun di luar JSON.

DATA TEKNIKAL {ticker}:

HARGA: Close={price.get('close')} | Open={price.get('open')} | High={price.get('high')} | Low={price.get('low')} | Perubahan={price.get('change_pct')}%

BREAKOUT: is_breakout={bo.get('is_breakout')} | tipe={bo.get('breakout_type')} | level={bo.get('breakout_level')} | jarak={bo.get('breakout_pct')}%
VOLUME: hari_ini={volume.get('today')} | avg_20d={volume.get('avg_20d')} | ratio={volume.get('ratio')}x | surge={volume.get('surge')}

SUPPORT/RESISTANCE: resistance={sr.get('nearest_resistance')} | support={sr.get('nearest_support')} | 52w_high={sr.get('high_52w')} | 52w_low={sr.get('low_52w')}

EMA: ema9={ema.get('ema9')} | ema21={ema.get('ema21')} | ema50={ema.get('ema50')} | ema200={ema.get('ema200')} | bullish_alignment={ema.get('bullish_alignment')} | above_ema200={ema.get('price_above_200')}

RSI(14): value={rsi.get('value')} | zone={rsi.get('zone')} | direction={rsi.get('direction')}
MACD(12,26,9): macd={macd.get('macd')} | signal={macd.get('signal')} | histogram={macd.get('histogram')} | bullish_cross={macd.get('bullish_cross')} | hist_growing={macd.get('histogram_growing')}
BBANDS(20,2): upper={bb.get('upper')} | mid={bb.get('mid')} | lower={bb.get('lower')} | squeeze={bb.get('squeeze')} | breakout_upper={bb.get('price_above_upper')}
STOCHASTIC: k={stoch.get('k')} | d={stoch.get('d')} | bullish_cross={stoch.get('bullish_cross')}
MFI(14): value={mfi.get('value')} | zone={mfi.get('zone')}
OBV: above_ema={obv.get('above_ema')} | rising={obv.get('rising')}
VWAP(20d): value={vwap.get('value_20d')} | price_above={vwap.get('price_above')}
ATR(14): value={atr.get('value')} | pct={atr.get('pct_of_price')}%

Berikan response JSON persis seperti ini:
{{
  "ticker": "{ticker}",
  "score": <0-100>,
  "signal": "<STRONG_BUY|BUY|NEUTRAL|AVOID>",
  "confidence": "<HIGH|MEDIUM|LOW>",
  "summary": "<2-3 kalimat Bahasa Indonesia>",
  "reasoning": {{
    "breakout_price": {{"score": <0-{SCORE_WEIGHTS['breakout_price']}>, "note": "<singkat>"}},
    "volume_surge": {{"score": <0-{SCORE_WEIGHTS['volume_surge']}>, "note": "<singkat>"}},
    "rsi_momentum": {{"score": <0-{SCORE_WEIGHTS['rsi_momentum']}>, "note": "<singkat>"}},
    "macd_signal": {{"score": <0-{SCORE_WEIGHTS['macd_signal']}>, "note": "<singkat>"}},
    "ema_alignment": {{"score": <0-{SCORE_WEIGHTS['ema_alignment']}>, "note": "<singkat>"}},
    "bbands_squeeze": {{"score": <0-{SCORE_WEIGHTS['bbands_squeeze']}>, "note": "<singkat>"}},
    "stoch_mfi": {{"score": <0-{SCORE_WEIGHTS['stoch_mfi']}>, "note": "<singkat>"}}
  }},
  "entry_zone": {{
    "ideal_entry": <harga>,
    "entry_range_low": <harga>,
    "entry_range_high": <harga>
  }},
  "risk_management": {{
    "stop_loss": <harga>,
    "stop_loss_pct": <angka>,
    "target_1": <harga>,
    "target_1_pct": <angka>,
    "target_2": <harga>,
    "target_2_pct": <angka>,
    "risk_reward_ratio": <angka>
  }},
  "warnings": ["<peringatan jika ada>"],
  "catalysts": ["<faktor positif>"],
  "timeframe": "<misal: 3-7 hari>"
}}

Panduan:
- STRONG_BUY: score >= 80
- BUY: score 65-79
- NEUTRAL: score 45-64
- AVOID: score < 45
- Volume konfirmasi sangat penting untuk breakout IDX
- Stop loss = 1x ATR di bawah entry atau di bawah support
"""
    return prompt.strip()


def analyze_with_ai(data: dict) -> Optional[dict]:
    ticker = data.get("ticker", "UNKNOWN")
    raw_text = ""

    try:
        prompt = build_analysis_prompt(data)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Kamu analis teknikal saham IDX profesional. "
                        "Jawab HANYA dengan JSON valid. "
                        "Jangan tambahkan teks, markdown, atau backtick apapun di luar JSON."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1500,
        )

        raw_text = response.choices[0].message.content.strip()

        # Bersihkan backtick jika ada
        if "```" in raw_text:
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
        raw_text = raw_text.strip()

        result = json.loads(raw_text)
        result["ticker"] = ticker

        logger.info(f"[{ticker}] Groq Score: {result.get('score')}/100 — {result.get('signal')}")
        return result

    except json.JSONDecodeError as e:
        logger.error(f"[{ticker}] Gagal parse JSON: {e} | Raw: {raw_text[:300]}")
        return None
    except Exception as e:
        logger.error(f"[{ticker}] Error Groq: {e}", exc_info=True)
        return None


def should_send_alert(ai_result: dict) -> bool:
    if not ai_result:
        return False
    score  = ai_result.get("score", 0)
    signal = ai_result.get("signal", "NEUTRAL")
    return score >= MIN_SCORE and signal in ("STRONG_BUY", "BUY")
