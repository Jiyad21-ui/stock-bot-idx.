# 📈 Stock Breakout Bot IDX

Bot analisa saham IDX otomatis dengan AI (Claude) yang mengirimkan alert ke Telegram
saat ada saham yang breakout dari level kunci dengan konfirmasi multi-indikator.

---

## ✨ Fitur

- **Multi-Indikator Teknikal**: EMA 9/21/50/200, RSI, MACD, Bollinger Bands, Stochastic, MFI, OBV, VWAP, ATR, Volume Surge
- **AI Scoring Claude**: Setiap saham dinilai 0–100 oleh Claude AI dengan reasoning
- **Breakout Detection**: Deteksi breakout resistance, 52-week high, near-breakout
- **Alert Telegram**: Pesan lengkap dengan entry zone, stop loss, target 1 & 2, risk/reward ratio
- **Anti-Spam Cooldown**: Ticker yang sama tidak dikirim ulang sebelum N hari
- **EOD Scan Otomatis**: Scan setiap hari setelah penutupan IDX (default 15:45 WIB)

---

## 🚀 Setup (5 Langkah)

### Langkah 1 — Clone & Install

```bash
cd stock-bot
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Langkah 2 — Buat Telegram Bot

1. Buka Telegram, cari **@BotFather**
2. Ketik `/newbot` dan ikuti instruksinya
3. Salin **Bot Token** yang diberikan

### Langkah 3 — Dapatkan Chat ID

1. Cari **@userinfobot** di Telegram
2. Start bot → kamu akan dapat Chat ID kamu
3. Atau buat group, tambahkan bot kamu ke group, lalu cek ID group via @getmyid_bot

### Langkah 4 — Isi Konfigurasi

```bash
cp .env.example .env
```

Edit file `.env`:
```
TELEGRAM_BOT_TOKEN=token_dari_botfather
TELEGRAM_CHAT_ID=id_chat_kamu
ANTHROPIC_API_KEY=key_dari_anthropic
```

### Langkah 5 — Test & Jalankan

```bash
# Test semua koneksi dulu
python main.py test

# Scan manual sekarang (tanpa tunggu jadwal)
python main.py scan

# Scan ticker tertentu
python main.py scan BBCA TLKM BBRI

# Jalankan scheduler (otomatis scan setiap hari)
python main.py
```

---

## ⚙️ Kustomisasi

### Tambah/Hapus Saham di Watchlist

Edit `config.py`:
```python
WATCHLIST = [
    "BBCA.JK", "BBRI.JK", "TLKM.JK",
    "TICKER_BARU.JK",  # tambah di sini
]
```

### Ubah Waktu Scan

Edit `config.py`:
```python
SCAN_TIME_WIB = "16:00"   # jam berapa setelah IDX tutup
```

### Ubah Minimum Score untuk Alert

```python
MIN_SCORE = 70   # 0–100, naikan untuk lebih selektif
```

### Ubah Cooldown

```python
ALERT_COOLDOWN_DAYS = 3   # hari sebelum ticker yang sama bisa alert lagi
```

---

## 📱 Contoh Alert Telegram

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 BREAKOUT ALERT — BBCA.JK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 Harga: 9,650 🔺 2.1%
📅 Tanggal: 2025-01-15

🎯 Sinyal: STRONG_BUY  🟢 HIGH
📊 Score Konfluensi:
████████░░ 82/100

💬 Analisis:
BBCA breakout dari resistance 9,500 dengan volume 2.3x rata-rata, 
didukung EMA bullish alignment dan RSI di zona kuat 62...

🚨 DETAIL BREAKOUT
  • Tipe: Breakout Resistance
  • Level: 9,500
  • Volume Ratio: 2.3x avg
  • Volume Surge: ✅

🎯 ENTRY & MANAJEMEN RISIKO
  • Zona Entry: 9,600 — 9,700
  • Stop Loss: 9,250 (-4.1%)
  • Target 1: 10,200 (+5.7%)
  • Target 2: 10,800 (+11.9%)
  • Risk/Reward: 2.5:1
  • Timeframe: 1-2 minggu
```

---

## 🗂️ Struktur File

```
stock-bot/
├── main.py               # Entry point + scheduler
├── config.py             # Semua konfigurasi
├── scanner.py            # Orkestrasi pipeline
├── data_fetcher.py       # Ambil data dari Yahoo Finance
├── technical_analysis.py # Hitung semua indikator teknikal
├── ai_scorer.py          # Scoring dengan Claude AI
├── telegram_notifier.py  # Format & kirim alert Telegram
├── cooldown_manager.py   # Cegah spam alert
├── requirements.txt      # Python dependencies
├── .env.example          # Template konfigurasi
├── .env                  # Konfigurasi kamu (jangan di-commit!)
├── data/
│   └── sent_alerts.json  # Riwayat alert (auto-generated)
└── logs/
    └── bot.log           # Log harian (auto-generated)
```

---

## 🐛 Troubleshooting

**Error: `ModuleNotFoundError`**
→ Pastikan virtual environment aktif dan sudah `pip install -r requirements.txt`

**Telegram: "Unauthorized"**
→ Cek TELEGRAM_BOT_TOKEN di `.env`

**Telegram: "Chat not found"**
→ Cek TELEGRAM_CHAT_ID. Untuk group, ID biasanya negatif (misal: -1001234567890)

**Yahoo Finance: data kosong**
→ Ticker IDX harus format `XXXX.JK`. Cek apakah saham masih aktif di IDX.

**AI tidak jalan**
→ Cek ANTHROPIC_API_KEY dan saldo kredit di console.anthropic.com

---

## ⚠️ Disclaimer

Bot ini dibuat untuk tujuan edukasi dan riset. Bukan merupakan rekomendasi investasi.
Selalu lakukan analisis sendiri (DYOR) sebelum mengambil keputusan investasi.
Investasi saham mengandung risiko kehilangan modal.

---

*Powered by Claude AI + Yahoo Finance + Telegram*
