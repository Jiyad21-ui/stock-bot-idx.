
"""
config.py — Konfigurasi utama Stock Breakout Bot IDX
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ─── Telegram ────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "")

# ─── Anthropic Claude ────────────────────────────────────────
ANTHROPIC_API_KEY  = os.getenv("ANTHROPIC_API_KEY", "")

# ─── Jadwal Scan EOD ─────────────────────────────────────────
SCAN_TIME_WIB = "15:45"

# ─── Filter Sinyal ───────────────────────────────────────────
MIN_SCORE = 70
BREAKOUT_CONFIRM_VOLUME = 1.5

# ─── Watchlist Saham IDX ─────────────────────────────────────
WATCHLIST = [

    # ══ KONGLOMERAT ════════════════════════════════════════
    "BRPT.JK", "BREN.JK", "TPIA.JK", "CDIA.JK", "PTRO.JK",
    "SSIA.JK","CUAN.JK",

    "RAJA.JK", "RATU.JK", "BUVA.JK", "MINA.JK",
    "PSKT.JK", "PADI.JK",

    "BUMI.JK", "ENRG.JK", "UNSP.JK", "BNBR.JK",
    "VKTR.JK", "DEWA.JK",

    "INKP.JK", "TKIM.JK", "FASW.JK", "SMAR.JK",
    "SSMS.JK", "SMGR.JK",

    "ICBP.JK", "INDF.JK", "SIMP.JK", "LSIP.JK",
    "DCII.JK",

    "DATA.JK", "UNTR.JK", "AUTO.JK", "BFIN.JK",

    "ASII.JK", "ASGR.JK", "TURI.JK", "AMFG.JK",
    "ABMM.JK",

    "LPKR.JK", "MPPA.JK", "SILO.JK", "MLPL.JK",

    "MNCN.JK", "BHIT.JK", "BMTR.JK",

    "ADRO.JK", "ADMR.JK", "ADCP.JK",

    "PGUN.JK", "JARR.JK", "CUAN.JK",

    "MAPI.JK", "ACES.JK", "CMPP.JK",

    "MEDC.JK", "ESSA.JK", "BIPI.JK",

    # ══ ENERGI ═════════════════════════════════════════════
    "PGAS.JK", "ELSA.JK", "RUIS.JK", "SURE.JK",
    "KEEN.JK", "TOBA.JK", "PTBA.JK", "ITMG.JK",
    "HRUM.JK", "GEMS.JK", "DSSA.JK", "MBAP.JK",
    "SMMT.JK", "MYOH.JK", "ARII.JK", "INDY.JK",

    # ══ TAMBANG ════════════════════════════════════════════
    "ANTM.JK", "INCO.JK", "MDKA.JK", "AMMN.JK",
    "MBMA.JK", "NCKL.JK", "TINS.JK", "DKFT.JK",
    "ZINC.JK", "PSAB.JK", "IFSH.JK", "KDTN.JK",

    # ══ PROPERTI ═══════════════════════════════════════════
    "BSDE.JK", "SMRA.JK", "PWON.JK", "CTRA.JK",
    "DILD.JK", "APLN.JK", "JRPT.JK", "BEST.JK",
    "MTLA.JK", "KIJA.JK", "GPRA.JK", "MDLN.JK",
    "NIRO.JK", "DUTI.JK", "OMRE.JK", "ASRI.JK",
    "JIHD.JK",

    # ══ INFRASTRUKTUR ══════════════════════════════════════
    "JSMR.JK", "WIKA.JK", "PTPP.JK", "WSKT.JK",
    "WEGE.JK", "ADHI.JK", "NRCA.JK", "TOTL.JK",
    "IDPR.JK", "PBSA.JK", "ACST.JK",

    # ══ PERKAPALAN ═════════════════════════════════════════
    "SMDR.JK", "TMAS.JK", "HITS.JK", "GTSI.JK",
    "NELY.JK", "BULL.JK", "BLTA.JK", "SHIP.JK",
    "PTIS.JK", "IPCM.JK", "ALII.JK", "LEAD.JK",
    "WINS.JK", "KARW.JK", "TRUK.JK",

    # ══ TEKNOLOGI ══════════════════════════════════════════
    "GOTO.JK", "BUKA.JK", "EMTK.JK", "MTDL.JK",
    "MLPT.JK", "DMMX.JK", "IRSX.JK",
    "INET.JK", "CCSI.JK", "MORA.JK",

    # ══ CONSUMER ═══════════════════════════════════════════
    "UNVR.JK", "KLBF.JK", "MYOR.JK", "CPIN.JK",
    "JPFA.JK", "GOOD.JK", "SIDO.JK", "HMSP.JK",
    "GGRM.JK", "ULTJ.JK", "DLTA.JK", "SKBM.JK",
    "TBLA.JK", "STTP.JK", "CAMP.JK",
    "FAST.JK", "PZZA.JK",

    # ══ KESEHATAN ══════════════════════════════════════════
    "KAEF.JK", "MIKA.JK", "HEAL.JK", "PRDA.JK",
    "DVLA.JK", "TSPC.JK", "INAF.JK",
    "PYFA.JK",

    # ══ AGRIBISNIS ═════════════════════════════════════════
    "AALI.JK", "SGRO.JK", "DSNG.JK", "PALM.JK",
    "ANJT.JK", "BWPT.JK",

    # ══ RETAIL ═════════════════════════════════════════════
    "LPPF.JK", "RALS.JK", "AMRT.JK", "MIDI.JK",
    "CSAP.JK", "HERO.JK",

    # ══ MEDIA ══════════════════════════════════════════════
    "SCMA.JK", "FILM.JK", "KBLV.JK",

    # ══ EV ═════════════════════════════════════════════════
    "KETR.JK",

    # ══ CATALYST ══════════════════════════════════════════
    "JGLE.JK", "ELPI.JK", "COCO.JK", "BAJA.JK",
    "RMKO.JK", "SINI.JK",

    # ══ TELKO ══════════════════════════════════════════════
    "TLKM.JK", "EXCL.JK", "ISAT.JK",
    "TBIG.JK", "TOWR.JK", "MTEL.JK",
]

# ─── KLASIFIKASI SEKTOR ──────────────────────────────────────
SECTORS = {

    "konglomerat": [
        "BRPT.JK", "BREN.JK", "TPIA.JK", "CDIA.JK",
        "PTRO.JK", "SSIA.JK","CUAN.JK",

        "RAJA.JK", "RATU.JK", "BUVA.JK",
        "MINA.JK", "PSKT.JK", "PADI.JK",

        "BUMI.JK", "ENRG.JK", "UNSP.JK",
        "BNBR.JK", "VKTR.JK", "DEWA.JK",

        "INKP.JK", "TKIM.JK", "FASW.JK",
        "SMAR.JK", "SSMS.JK", "SMGR.JK",

        "ICBP.JK", "INDF.JK", "SIMP.JK",
        "LSIP.JK", "DCII.JK",

        "DATA.JK", "UNTR.JK", "AUTO.JK",
        "BFIN.JK",

        "ASII.JK", "ASGR.JK", "TURI.JK",
        "AMFG.JK", "ABMM.JK",

        "LPKR.JK", "MPPA.JK", "SILO.JK",
        "MLPL.JK",

        "MNCN.JK", "BHIT.JK", "BMTR.JK",

        "ADRO.JK", "ADMR.JK", "ADCP.JK",

        "PGUN.JK", "JARR.JK", "CUAN.JK",

        "MAPI.JK", "ACES.JK", "CMPP.JK",

        "MEDC.JK", "ESSA.JK", "BIPI.JK"
    ],
    "energi": [
        "PGAS.JK", "MEDC.JK", "ESSA.JK", "ELSA.JK", "RUIS.JK",
        "BIPI.JK", "ENRG.JK", "RAJA.JK", "SURE.JK", "BREN.JK",
        "KEEN.JK", "TOBA.JK", "ADRO.JK", "PTBA.JK", "ITMG.JK",
        "HRUM.JK", "GEMS.JK", "DSSA.JK", "MBAP.JK", "SMMT.JK",
        "MYOH.JK", "ARII.JK", "INDY.JK",
    ],

    "tambang": [
        "ANTM.JK", "INCO.JK", "MDKA.JK", "AMMN.JK", "MBMA.JK",
        "NCKL.JK", "TINS.JK", "PTBA.JK", "ITMG.JK", "HRUM.JK",
        "GEMS.JK", "ADRO.JK", "ADMR.JK", "DKFT.JK", "ZINC.JK",
        "PSAB.JK", "IFSH.JK", "KDTN.JK", "CUAN.JK",
    ],

    "properti": [
        "BSDE.JK", "SMRA.JK", "PWON.JK", "CTRA.JK", "LPKR.JK",
        "DILD.JK", "APLN.JK", "JRPT.JK", "BEST.JK", "MTLA.JK",
        "KIJA.JK", "GPRA.JK", "MDLN.JK", "NIRO.JK", "DUTI.JK",
        "OMRE.JK", "ASRI.JK", "BUVA.JK", "JIHD.JK",
    ],

    "infrastruktur": [
        "JSMR.JK", "WIKA.JK", "PTPP.JK", "WSKT.JK", "WEGE.JK",
        "ADHI.JK", "NRCA.JK", "TOTL.JK", "IDPR.JK", "PBSA.JK",
        "ACST.JK",
    ],

    "perkapalan": [
        "SMDR.JK", "TMAS.JK", "HITS.JK", "GTSI.JK", "NELY.JK",
        "BULL.JK", "BLTA.JK", "SHIP.JK", "PTIS.JK", "IPCM.JK",
        "ALII.JK", "LEAD.JK", "WINS.JK", "KARW.JK", "TRUK.JK",
    ],

    "teknologi": [
        "GOTO.JK", "BUKA.JK", "EMTK.JK", "DCII.JK", "DATA.JK",
        "MTDL.JK", "MLPT.JK", "DMMX.JK", "IRSX.JK", "VKTR.JK",
    ],

    "consumer": [
        "UNVR.JK", "KLBF.JK", "MYOR.JK", "CPIN.JK", "JPFA.JK",
        "GOOD.JK", "SIDO.JK", "HMSP.JK", "GGRM.JK", "ULTJ.JK",
        "DLTA.JK", "SKBM.JK", "TBLA.JK", "STTP.JK", "CAMP.JK",
        "FAST.JK", "PZZA.JK",
    ],

    "kesehatan": [
        "KAEF.JK", "MIKA.JK", "SILO.JK", "HEAL.JK", "PRDA.JK",
        "DVLA.JK", "TSPC.JK", "INAF.JK", "KLBF.JK",
    ],

    "agribisnis": [
        "AALI.JK", "LSIP.JK", "SGRO.JK", "SSMS.JK", "DSNG.JK",
        "PALM.JK", "ANJT.JK", "BWPT.JK", "SIMP.JK", "SMAR.JK",
        "PGUN.JK", "JARR.JK",
    ],

    "telko": [
        "TLKM.JK", "EXCL.JK", "ISAT.JK", "TBIG.JK",
        "TOWR.JK", "MTEL.JK",
    ],

    "retail": [
        "LPPF.JK", "RALS.JK", "AMRT.JK", "MIDI.JK",
        "CSAP.JK", "HERO.JK", "MAPI.JK", "ACES.JK",
    ],

    "media": [
        "MNCN.JK", "SCMA.JK", "BMTR.JK", "EMTK.JK",
        "FILM.JK", "KBLV.JK", "RCTI.JK",
    ],

    "ev": [
        "VKTR.JK", "BREN.JK", "TOBA.JK", "NCKL.JK",
        "MBMA.JK", "KDTN.JK", "AMMN.JK",
    ],

  "catalyst": [
    "TOBA.JK", "KDTN.JK", "IRSX.JK", "JGLE.JK", "ELPI.JK",
    "COCO.JK", "BAJA.JK", "RMKO.JK", "BUVA.JK", "MINA.JK",
    "PADI.JK", "PSKT.JK", "RATU.JK", "BNBR.JK", "MPPA.JK",
    "VKTR.JK", "INET.JK", "SINI.JK", "BUMI.JK", "CCSI.JK",
    "MORA.JK", "KETR.JK", "PYFA.JK"
]
}


# ─── Parameter Indikator Teknikal ────────────────────────────
INDICATORS = {
    "ema_fast": 9,
    "ema_mid": 21,
    "ema_slow": 50,
    "ema_trend": 200,

    "rsi_period": 14,

    "macd_fast": 12,
    "macd_slow": 26,
    "macd_signal": 9,

    "bbands_period": 20,
    "bbands_std": 2,

    "atr_period": 14,

    "stoch_k": 14,
    "stoch_d": 3,

    "mfi_period": 14,

    "obv_ema": 21,

    "volume_avg_days": 20,

    "sr_lookback": 60,

    "data_period": "1y",
}

# ─── Scoring Weights ─────────────────────────────────────────
SCORE_WEIGHTS = {
    "breakout_price": 25,
    "volume_surge": 20,
    "rsi_momentum": 15,
    "macd_signal": 15,
    "ema_alignment": 15,
    "bbands_squeeze": 5,
    "stoch_mfi": 5,
}

# ─── Cooldown ────────────────────────────────────────────────
ALERT_COOLDOWN_DAYS = 3
COOLDOWN_FILE = "data/sent_alerts.json"

# ─── Logging ─────────────────────────────────────────────────
LOG_FILE = "logs/bot.log"
LOG_LEVEL = "INFO"

