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

    prompt = (
        f"Kamu adalah analis teknikal saham senior spesialis pasar IDX Indonesia.\n"
        f"Jawab HANYA dengan JSON valid, tanpa teks apapun di luar JSON.\n\n"
        f"DATA TEKNIKAL {ticker}:\n\n"
        f"HARGA: Close={price.get('close')} | Open={price.get('open')} | "
        f"High={price.get('high')} | Low={price.get('low')} | Perubahan={price.get('change_pct')}%\n\n"
        f"BREAKOUT: is_breakout={bo.get('is_breakout')} | tipe={bo.get('breakout_type')} | "
        f"level={bo.get('breakout_level')} | jarak={bo.get('breakout_pct')}%\n"
        f"VOLUME: hari_ini={volume.get('today')} | avg_20d={volume.get('avg_20d')} | "
        f"ratio={volume.get('ratio')}x | surge={volume.get('surge')}\n\n"
        f"SUPPORT DAN RESISTANCE: resistance={sr.get('nearest_resistance')} | "
        f"support={sr.get('nearest_support')} | high_52w={sr.get('high_52w')} | "
        f"low_52w={sr.get('low_52w')}\n\n"
        f"EMA: ema9={ema.get('ema9')} | ema21={ema.get('ema21')} | "
        f"ema50={ema.get('ema50')} | ema200={ema.get('ema200')} | "
        f"bullish_alignment={ema.get('bullish_alignment')} | above_ema200={ema.get('price_above_200')}\n\n"
        f"RSI(14): value={rsi.get('value')} | zone={rsi.get('zone')} | direction={rsi.get('direction')}\n"
        f"MACD(12,26,9): macd={macd.get('macd')} | signal={macd.get('signal')} | "
        f"histogram={macd.get('histogram')} | bullish_cross={macd.get('bullish_cross')} | "
        f"hist_growing={macd.get('histogram_growing')}\n"
        f"BBANDS(20,2): upper={bb.get('upper')} | mid={bb.get('mid')} | lower={bb.get('lower')} | "
        f"squeeze={bb.get('squeeze')} | breakout_upper={bb.get('price_above_upper')}\n"
        f"STOCHASTIC: k={stoch.get('k')} | d={stoch.get('d')} | bullish_cross={stoch.get('bullish_cross')}\n"
        f"MFI(14): value={mfi.get('value')} | zone={mfi.get('zone')}\n"
        f"OBV: above_ema={obv.get('above_ema')} | rising={obv.get('rising')}\n"
        f"VWAP(20d): value={vwap.get('value_20d')} | price_above={vwap.get('price_above')}\n"
        f"ATR(14): value={atr.get('value')} | pct={atr.get('pct_of_price')}%\n\n"
        f"Berikan response JSON persis seperti ini:\n"
        f"{{\n"
        f'  "ticker": "{ticker}",\n'
        f'  "score": <0-100>,\n'
        f'  "signal": "<STRONG_BUY|BUY|NEUTRAL|AVOID>",\n'
        f'  "confidence": "<HIGH|MEDIUM|LOW>",\n'
        f'  "summary": "<2-3 kalimat Bahasa Indonesia>",\n'
        f'  "reasoning": {{\n'
        f'    "breakout_price": {{"score": <0-{SCORE_WEIGHTS["breakout_price"]}>, "note": "<singkat>"}},\n'
        f'    "volume_surge": {{"score": <0-{SCORE_WEIGHTS["volume_surge"]}>, "note": "<singkat>"}},\n'
        f'    "rsi_momentum": {{"score": <0-{SCORE_WEIGHTS["rsi_momentum"]}>, "note": "<singkat>"}},\n'
        f'    "macd_signal": {{"score": <0-{SCORE_WEIGHTS["macd_signal"]}>, "note": "<singkat>"}},\n'
        f'    "ema_alignment": {{"score": <0-{SCORE_WEIGHTS["ema_alignment"]}>, "note": "<singkat>"}},\n'
        f'    "bbands_squeeze": {{"score": <0-{SCORE_WEIGHTS["bbands_squeeze"]}>, "note": "<singkat>"}},\n'
        f'    "stoch_mfi": {{"score": <0-{SCORE_WEIGHTS["stoch_mfi"]}>, "note": "<singkat>"}}\n'
        f'  }},\n'
        f'  "entry_zone": {{\n'
        f'    "ideal_entry": <harga>,\n'
        f'    "entry_range_low": <harga>,\n'
        f'    "entry_range_high": <harga>\n'
        f'  }},\n'
        f'  "risk_management": {{\n'
        f'    "stop_loss": <harga>,\n'
        f'    "stop_loss_pct": <angka>,\n'
        f'    "target_1": <harga>,\n'
        f'    "target_1_pct": <angka>,\n'
        f'    "target_2": <harga>,\n'
        f'    "target_2_pct": <angka>,\n'
        f'    "risk_reward_ratio": <angka>\n'
        f'  }},\n'
        f'  "warnings": ["<peringatan jika ada>"],\n'
        f'  "catalysts": ["<faktor positif>"],\n'
        f'  "timeframe": "<misal: 3-7 hari>"\n'
        f"}}\n\n"
        f"Panduan:\n"
        f"- STRONG_BUY: score >= 80\n"
        f"- BUY: score 65-79\n"
        f"- NEUTRAL: score 45-64\n"
        f"- AVOID: score < 45\n"
        f"- Volume konfirmasi sangat penting untuk breakout IDX\n"
        f"- Stop loss = 1x ATR di bawah entry atau di bawah support\n"
    )
    return prompt.strip()


def analyze_with_ai(data: dict) -> Optional[dict]:
    ticker = data.get("ticker", "UNKNOWN")
    raw_text = ""

    try:
        prompt = build_analysis_prompt(data)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
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
