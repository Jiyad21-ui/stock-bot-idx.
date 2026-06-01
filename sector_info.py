"""
sector_info.py — Data lengkap emiten per sektor + narasi katalyst
"""

SECTOR_INFO = {

    "konglomerat": {
        "title": "🏢 KONGLOMERAT IDX",
        "description": "Saham-saham milik konglomerat besar Indonesia",
        "groups": {
            "🔵 PRAJOGO PANGESTU (Grup Barito)": {
                "tickers": ["BRPT.JK", "BREN.JK", "TPIA.JK", "CDIA.JK", "PTRO.JK", "SSIA.JK"],
                "info": "Raja petrokimia & energi terbarukan. BREN jadi primadona setelah IPO jumbo. TPIA dominasi industri petrokimia nasional."
            },
            "🟢 HAPPY HAPSORO (Grup Hapsoro)": {
                "tickers": ["RAJA.JK", "RATU.JK", "BUVA.JK", "MINA.JK", "PSKT.JK", "PADI.JK", "ARCI.JK"],
                "info": "Konglomerat baru yang agresif ekspansi. RAJA & RATU jadi motor utama. BUVA ekspansi properti premium Bali."
            },
            "🔴 GRUP BAKRIE": {
                "tickers": ["BUMI.JK", "ENRG.JK", "UNSP.JK", "BNBR.JK", "VKTR.JK", "DEWA.JK", "BKSL.JK"],
                "info": "Konglomerat legendaris. VKTR jadi andalan baru di sektor kendaraan listrik bus. BNBR induk grup sedang rights issue."
            },
            "⚫ GRUP SINARMAS (Eka Tjipta Widjaja)": {
                "tickers": ["INKP.JK", "TKIM.JK", "FASW.JK", "SMAR.JK", "SSMS.JK", "SMGR.JK", "DUTI.JK"],
                "info": "Raksasa pulp & kertas dunia. INKP & TKIM market leader global. SMGR dominasi semen nasional."
            },
            "🟡 GRUP SALIM (Anthony Salim)": {
                "tickers": ["ICBP.JK", "INDF.JK", "SIMP.JK", "LSIP.JK", "DCII.JK", "MLBI.JK"],
                "info": "Kerajaan consumer goods. Indomie ada di seluruh dunia. DCII jadi pemain data center terbesar Indonesia."
            },
            "🟤 GRUP DJARUM (Hartono Bersaudara)": {
                "tickers": ["DATA.JK", "UNTR.JK", "AUTO.JK", "BFIN.JK"],
                "info": "Pemilik BCA (non-listed di sini). UNTR raksasa alat berat. DATA ekspansi infrastruktur digital."
            },
            "⚪ GRUP ASTRA": {
                "tickers": ["ASII.JK", "ASGR.JK", "TURI.JK", "AMFG.JK", "ABMM.JK", "ACST.JK"],
                "info": "Konglomerat otomotif terbesar. ASII induk grup dengan diversifikasi bisnis terluas di Indonesia."
            },
            "🟣 GRUP LIPPO (Mochtar Riady)": {
                "tickers": ["LPKR.JK", "MPPA.JK", "SILO.JK", "LPLI.JK", "MLPL.JK"],
                "info": "Properti, retail, dan kesehatan. SILO jaringan RS terbesar. MPPA rights issue untuk akuisisi aset baru."
            },
            "🔶 GRUP MNC (Hary Tanoesoedibjo)": {
                "tickers": ["MNCN.JK", "BHIT.JK", "BMTR.JK", "RCTI.JK"],
                "info": "Raja media Indonesia. MNCN kuasai TV nasional. Ekspansi ke digital dan entertainment."
            },
            "🔷 GRUP ADARO (Garibaldi Thohir)": {
                "tickers": ["ADRO.JK", "ADMR.JK", "ADCP.JK", "MBSS.JK"],
                "info": "Raksasa batu bara & transisi energi. ADMR fokus mineral. ADCP ekspansi ke energi bersih."
            },
            "🟠 GRUP HAJI ISAM": {
                "tickers": ["PGUN.JK", "JARR.JK", "CUAN.JK", "HELI.JK"],
                "info": "Konglomerat Kalimantan. CUAN (Petrindo) ekspansi batu bara premium. JARR agribisnis sawit besar."
            },
            "🩷 GRUP CT CORP (Chairul Tanjung)": {
                "tickers": ["MAPI.JK", "ACES.JK", "CMPP.JK", "CNKO.JK"],
                "info": "Retail dan lifestyle. MAPI & ACES dominasi retail premium. CMPP operasikan AirAsia Indonesia."
            },
            "🩵 GRUP MEDCO (Arifin Panigoro)": {
                "tickers": ["MEDC.JK", "ESSA.JK", "BIPI.JK", "RUIS.JK"],
                "info": "Energi dan petrokimia. ESSA produksi amonia & LNG. MEDC ekspansi blok migas baru."
            },
            "🌿 GRUP HASHIM (Hashim Djojohadikusumo)": {
                "tickers": ["COIN.JK", "NCKL.JK", "ARCI.JK"],
                "info": "Adik Prabowo. NCKL (Trimegah) raksasa nikel Halmahera. Ekspansi agresif di mineral kritis."
            },
        }
    },

    "catalyst": {
        "title": "🔥 SAHAM CATALYST & NARASI PANAS 2026",
        "description": "Saham dengan katalis fundamental kuat yang sedang ramai dibicarakan",
        "groups": {
            "⚡ TOBA.JK — TBS Energi Utama": {
                "tickers": ["TOBA.JK"],
                "info": "Rights issue untuk ekspansi ekosistem EV Electrum (JV dengan Gojek). Transformasi dari batu bara ke energi terbarukan & baterai EV. Narasi transisi energi paling seksi 2026."
            },
            "🇨🇳 KDTN.JK — Kencana Darat": {
                "tickers": ["KDTN.JK"],
                "info": "Akuisisi 86% saham oleh Huayou Holdings (raksasa nikel & baterai China). Transformasi jadi emiten nikel-baterai EV. Potensi rerating valuasi signifikan."
            },
            "🤖 IRSX.JK — Folago Global": {
                "tickers": ["IRSX.JK"],
                "info": "Rights issue jumbo Rp3,71 triliun untuk ekspansi teknologi AI, media commerce, dan hiburan digital. Perubahan bisnis model total dari properti ke digital."
            },
            "🏠 MPPA.JK — Matahari Putra Prima": {
                "tickers": ["MPPA.JK"],
                "info": "Rights issue Rp780 miliar untuk akuisisi 6 aset properti baru. Restrukturisasi bisnis retail ke properti komersial."
            },
            "🔋 MBMA.JK — Merdeka Battery Materials": {
                "tickers": ["MBMA.JK"],
                "info": "Ekosistem baterai EV terintegrasi. Smelter nikel, kobalt, MHP. Mitra strategis pabrikan baterai Korea & China."
            },
            "⛏️ AMMN.JK — Amman Mineral": {
                "tickers": ["AMMN.JK"],
                "info": "Smelter tembaga & emas terbesar Indonesia mulai produksi penuh. Revenue dari emas & tembaga naik signifikan. Salah satu tambang terbesar dunia."
            },
            "💻 DCII.JK — DCI Indonesia": {
                "tickers": ["DCII.JK"],
                "info": "Data center terbesar Indonesia. Demand dari cloud provider global (AWS, Google, Azure) terus naik. Ekspansi kapasitas agresif 2026."
            },
            "🚌 VKTR.JK — VKTR Teknologi": {
                "tickers": ["VKTR.JK"],
                "info": "Bus listrik untuk TransJakarta & DAMRI. Kontrak pemerintah jumbo. Satu-satunya produsen bus EV lokal yang sudah beroperasi massal."
            },
            "🌱 BREN.JK — Barito Renewables": {
                "tickers": ["BREN.JK"],
                "info": "Energi terbarukan terbesar Indonesia. Panas bumi, angin, surya. Narasi green energy global. Valuasi premium tapi pertumbuhan kencang."
            },
            "🏗️ NCKL.JK — Trimegah Bangun Persada": {
                "tickers": ["NCKL.JK"],
                "info": "Nikel terbesar Halmahera. Supply chain baterai EV global. Mitra CATL & pabrikan Korea. Ekspansi kapasitas smelter terus berjalan."
            },
            "🛢️ ESSA.JK — ESSA Industries": {
                "tickers": ["ESSA.JK"],
                "info": "Produser amonia & LNG. Demand pupuk & energi global naik. Ekspansi kapasitas pabrik amonia tahap 2 sedang berjalan."
            },
            "🎰 ELPI.JK": {
                "tickers": ["ELPI.JK"],
                "info": "Rights issue 2026 untuk ekspansi bisnis. Monitor aksi korporasi lebih lanjut."
            },
            "🏢 BNBR.JK — Bakrie & Brothers": {
                "tickers": ["BNBR.JK"],
                "info": "Rights issue untuk pendanaan proyek jalan tol baru. Induk grup Bakrie sedang restrukturisasi bisnis."
            },
            "🌊 RAJA.JK — Rukun Raharja": {
                "tickers": ["RAJA.JK"],
                "info": "Infrastruktur gas & energi. Ekspansi jaringan distribusi gas. Bagian dari portofolio Hapsoro yang agresif."
            },
            "🏨 BUVA.JK — Bukit Uluwatu Villa": {
                "tickers": ["BUVA.JK"],
                "info": "Properti premium Bali. Ekspansi resort & villa mewah. Beneficiary pemulihan pariwisata internasional ke Bali."
            },
        }
    },

    "energi": {
        "title": "⚡ SEKTOR ENERGI IDX",
        "description": "Minyak & Gas, Batu Bara, dan Energi Terbarukan",
        "groups": {
            "🛢️ Minyak & Gas": {
                "tickers": ["PGAS.JK", "MEDC.JK", "ESSA.JK", "ELSA.JK", "RUIS.JK", "BIPI.JK", "ENRG.JK"],
                "info": "PGAS distribusi gas nasional. MEDC ekspansi blok migas. ESSA produksi amonia dari gas alam."
            },
            "🔥 Batu Bara Thermal": {
                "tickers": ["ADRO.JK", "PTBA.JK", "ITMG.JK", "HRUM.JK", "GEMS.JK", "DSSA.JK", "MBAP.JK", "MYOH.JK", "ARII.JK", "SMMT.JK"],
                "info": "PTBA & ITMG blue chip batu bara. Harga batu bara masih tinggi. ADRO diversifikasi ke EV & energi bersih."
            },
            "🌱 Energi Terbarukan": {
                "tickers": ["BREN.JK", "KEEN.JK", "TOBA.JK", "RAJA.JK", "SURE.JK"],
                "info": "BREN panas bumi terbesar. TOBA transformasi ke EV & baterai. Narasi transisi energi jadi motor utama."
            },
        }
    },

    "tambang": {
        "title": "⛏️ SEKTOR TAMBANG & MINERAL IDX",
        "description": "Emas, Tembaga, Nikel, Timah, dan Mineral Kritis",
        "groups": {
            "🥇 Emas & Tembaga": {
                "tickers": ["MDKA.JK", "AMMN.JK", "ANTM.JK", "PSAB.JK"],
                "info": "AMMN smelter tembaga-emas terbesar. MDKA Merdeka Copper Gold ekspansi agresif. Harga emas global di level tertinggi."
            },
            "🔋 Nikel & Baterai EV": {
                "tickers": ["INCO.JK", "MBMA.JK", "NCKL.JK", "IFSH.JK", "DKFT.JK", "KDTN.JK"],
                "info": "Indonesia kuasai 40% nikel dunia. NCKL & MBMA supply chain baterai EV global. KDTN diakuisisi Huayou China."
            },
            "🪙 Timah & Zinc": {
                "tickers": ["TINS.JK", "ZINC.JK"],
                "info": "TINS produsen timah terbesar dunia. Harga timah naik seiring demand elektronik global."
            },
            "⚫ Batu Bara Metalurgi": {
                "tickers": ["PTBA.JK", "ITMG.JK", "HRUM.JK", "GEMS.JK", "ADMR.JK", "CUAN.JK"],
                "info": "Batu bara kokas untuk industri baja. ADMR (Adaro Minerals) fokus batu bara premium metalurgi."
            },
        }
    },

    "properti": {
        "title": "🏠 SEKTOR PROPERTI IDX",
        "description": "Developer properti, kawasan industri, dan REIT",
        "groups": {
            "🏙️ Developer Besar": {
                "tickers": ["BSDE.JK", "SMRA.JK", "PWON.JK", "CTRA.JK", "LPKR.JK"],
                "info": "Big 5 properti Indonesia. BSDE BSD City terluas. PWON mall & mixed-use Surabaya. Beneficiary suku bunga turun."
            },
            "🏭 Kawasan Industri": {
                "tickers": ["BEST.JK", "KIJA.JK", "SSIA.JK", "DILD.JK"],
                "info": "Demand kavling industri naik dari relokasi pabrik China ke Indonesia. BEST & KIJA paling banyak diincar investor asing."
            },
            "🏨 Hotel & Komersial": {
                "tickers": ["JIHD.JK", "BUVA.JK", "JRPT.JK", "OMRE.JK"],
                "info": "Recovery pariwisata dorong occupancy rate hotel. BUVA properti premium Bali terus ekspansi."
            },
            "🏘️ Mid Cap Properti": {
                "tickers": ["MTLA.JK", "GPRA.JK", "MDLN.JK", "NIRO.JK", "APLN.JK", "ASRI.JK"],
                "info": "Segmen perumahan menengah. Beneficiary program 3 juta rumah pemerintah Prabowo."
            },
        }
    },

    "perkapalan": {
        "title": "⚓ SEKTOR PERKAPALAN & LOGISTIK LAUT IDX",
        "description": "Pelayaran, logistik laut, dan infrastruktur pelabuhan",
        "groups": {
            "🚢 Pelayaran Besar": {
                "tickers": ["SMDR.JK", "TMAS.JK", "HITS.JK", "BULL.JK"],
                "info": "SMDR Samudera Indonesia konglomerat pelayaran. BULL ekspansi armada tanker. Freight rate global masih tinggi."
            },
            "⛽ Tanker & Offshore": {
                "tickers": ["BLTA.JK", "WINS.JK", "PTIS.JK", "LEAD.JK"],
                "info": "BLTA Berlian Laju Tanker restrukturisasi. WINS offshore support vessel migas. Demand tinggi seiring aktivitas migas."
            },
            "🏗️ Infrastruktur Pelabuhan": {
                "tickers": ["IPCM.JK", "KARW.JK", "ALII.JK"],
                "info": "IPCM Jasa Armada Indonesia jasa pelabuhan. Beneficiary peningkatan volume ekspor impor."
            },
            "🚤 Armada Kecil & Logistik": {
                "tickers": ["GTSI.JK", "NELY.JK", "SHIP.JK", "TRUK.JK"],
                "info": "Pelayaran regional dan logistik last mile. GTSI grup Humpuss ekspansi armada."
            },
        }
    },

    "teknologi": {
        "title": "💻 SEKTOR TEKNOLOGI & DIGITAL IDX",
        "description": "Startup tech, data center, dan infrastruktur digital",
        "groups": {
            "📱 Super App & E-commerce": {
                "tickers": ["GOTO.JK", "BUKA.JK"],
                "info": "GOTO (Gojek-Tokopedia) menuju profitabilitas. BUKA masih berjuang. Narasi profitabilitas jadi kunci rerating."
            },
            "🖥️ Data Center & Cloud": {
                "tickers": ["DCII.JK", "DATA.JK", "MTDL.JK", "MLPT.JK"],
                "info": "DCII data center terbesar demand dari hyperscaler global. Era AI dorong kebutuhan data center meledak."
            },
            "📺 Media & Konten Digital": {
                "tickers": ["EMTK.JK", "IRSX.JK", "DMMX.JK"],
                "info": "EMTK induk Vidio & media digital. IRSX transformasi ke AI & media commerce dengan rights issue jumbo."
            },
            "🚗 Teknologi Transportasi": {
                "tickers": ["VKTR.JK"],
                "info": "VKTR satu-satunya produsen bus EV lokal. Kontrak TransJakarta & DAMRI. Narasi elektrifikasi transportasi publik."
            },
        }
    },

    "ev": {
        "title": "🔋 SEKTOR EV & ENERGI TERBARUKAN IDX",
        "description": "Kendaraan listrik, baterai, nikel, dan green energy",
        "groups": {
            "🚗 Kendaraan Listrik": {
                "tickers": ["VKTR.JK", "TOBA.JK"],
                "info": "VKTR bus EV. TOBA via Electrum (JV Gojek) bangun ekosistem baterai & motor listrik."
            },
            "🔋 Baterai & Material": {
                "tickers": ["MBMA.JK", "NCKL.JK", "KDTN.JK", "AMMN.JK"],
                "info": "Supply chain baterai EV. MBMA ekosistem terintegrasi. NCKL nikel terbesar. KDTN diakuisisi Huayou China."
            },
            "🌿 Green Energy": {
                "tickers": ["BREN.JK", "KEEN.JK", "ADCP.JK"],
                "info": "BREN panas bumi & angin terbesar. KEEN panel surya. ADCP (Adaro Clean Energy) transisi hijau."
            },
        }
    },

    "consumer": {
        "title": "🛒 SEKTOR CONSUMER GOODS IDX",
        "description": "Makanan, minuman, rokok, dan kebutuhan sehari-hari",
        "groups": {
            "🍜 Makanan & Minuman": {
                "tickers": ["ICBP.JK", "INDF.JK", "MYOR.JK", "GOOD.JK", "ULTJ.JK", "DLTA.JK", "SKBM.JK", "STTP.JK", "CAMP.JK"],
                "info": "ICBP Indomie raja mie instan dunia. MYOR Mayora ekspansi global. Sektor defensif tahan resesi."
            },
            "🚬 Rokok": {
                "tickers": ["HMSP.JK", "GGRM.JK", "WIIM.JK"],
                "info": "HMSP HM Sampoerna & GGRM Gudang Garam raksasa rokok. Tekanan regulasi tapi cashflow masif."
            },
            "🐔 Peternakan & Pakan": {
                "tickers": ["CPIN.JK", "JPFA.JK", "GOOD.JK"],
                "info": "CPIN Charoen Pokphand dominasi industri ayam broiler. Siklus harga ayam jadi penentu utama kinerja."
            },
            "🌿 Herbal & Kesehatan": {
                "tickers": ["SIDO.JK", "KLBF.JK"],
                "info": "SIDO Muncul Tolak Angin brand ikonik. Ekspansi ekspor herbal ke ASEAN & Timteng."
            },
        }
    },

    "kesehatan": {
        "title": "🏥 SEKTOR KESEHATAN IDX",
        "description": "Rumah sakit, farmasi, dan layanan kesehatan",
        "groups": {
            "🏥 Jaringan RS": {
                "tickers": ["MIKA.JK", "SILO.JK", "HEAL.JK"],
                "info": "SILO Siloam RS terbanyak Indonesia. MIKA Mitra Keluarga premium. HEAL ekspansi agresif tier 2-3."
            },
            "💊 Farmasi": {
                "tickers": ["KAEF.JK", "KLBF.JK", "DVLA.JK", "TSPC.JK", "INAF.JK", "PYFA.JK"],
                "info": "KAEF Kimia Farma BUMN farmasi. KLBF Kalbe terbesar. Beneficiary program JKN & kesadaran kesehatan pasca COVID."
            },
            "🔬 Diagnostik": {
                "tickers": ["PRDA.JK", "SCPI.JK"],
                "info": "PRDA Prodia laboratorium klinik terbesar. Demand pemeriksaan kesehatan rutin terus naik."
            },
        }
    },

    "agribisnis": {
        "title": "🌴 SEKTOR AGRIBISNIS IDX",
        "description": "Kelapa sawit, perkebunan, dan pertanian",
        "groups": {
            "🌴 Kelapa Sawit Besar": {
                "tickers": ["AALI.JK", "LSIP.JK", "SGRO.JK", "SSMS.JK", "DSNG.JK"],
                "info": "AALI Astra Agro terbesar. Harga CPO dipengaruhi supply Malaysia & demand biodiesel B35-B40."
            },
            "🌱 Sawit Mid Cap": {
                "tickers": ["PALM.JK", "ANJT.JK", "BWPT.JK", "SIMP.JK", "SMAR.JK"],
                "info": "Pemain sawit menengah dengan potensi upside lebih besar. Beneficiary kenaikan harga CPO global."
            },
            "🐖 Agribisnis Lain": {
                "tickers": ["PGUN.JK", "JARR.JK"],
                "info": "JARR Jhonlin Agro sawit Kalimantan. PGUN Pradiksi Gunatama ekspansi perkebunan."
            },
        }
    },

    "telko": {
        "title": "📡 SEKTOR TELEKOMUNIKASI IDX",
        "description": "Operator telko, menara, dan infrastruktur digital",
        "groups": {
            "📱 Operator Telko": {
                "tickers": ["TLKM.JK", "EXCL.JK", "ISAT.JK"],
                "info": "TLKM Telkom BUMN dominan. ISAT Indosat pasca merger Ooredoo. Persaingan tarif data masih ketat."
            },
            "📡 Menara Telko": {
                "tickers": ["TBIG.JK", "TOWR.JK", "MTEL.JK"],
                "info": "Tower sharing bisnis recurring revenue stabil. TBIG & TOWR terbesar. Demand 5G dorong kebutuhan menara baru."
            },
        }
    },

    "retail": {
        "title": "🛍️ SEKTOR RETAIL IDX",
        "description": "Ritel modern, fashion, dan consumer lifestyle",
        "groups": {
            "🏪 Minimarket & Supermarket": {
                "tickers": ["AMRT.JK", "MIDI.JK", "HERO.JK", "MPPA.JK"],
                "info": "AMRT Alfamart ekspansi 1000+ gerai/tahun. MIDI Alfamidi terus tumbuh. Beneficiary konsumsi domestik."
            },
            "👗 Fashion & Lifestyle": {
                "tickers": ["MAPI.JK", "LPPF.JK", "RALS.JK", "CSAP.JK"],
                "info": "MAPI Mitra Adiperkasa brand premium. LPPF Matahari Dept Store restrukturisasi. Recovery mall pasca COVID."
            },
            "🔧 Home & Hardware": {
                "tickers": ["ACES.JK"],
                "info": "ACES Ace Hardware ekspansi ke kota tier 2-3. Beneficiary boom properti dan renovasi rumah."
            },
        }
    },

    "infrastruktur": {
        "title": "🏗️ SEKTOR INFRASTRUKTUR IDX",
        "description": "Konstruksi, jalan tol, dan infrastruktur publik",
        "groups": {
            "🛣️ Jalan Tol": {
                "tickers": ["JSMR.JK"],
                "info": "JSMR Jasa Marga operator tol terbesar. Revenue tumbuh seiring volume kendaraan. Ekspansi ruas baru Trans Jawa."
            },
            "🏢 BUMN Konstruksi": {
                "tickers": ["WIKA.JK", "PTPP.JK", "WSKT.JK", "ADHI.JK"],
                "info": "4 BUMN konstruksi. WSKT & WIKA masih restrukturisasi utang. PTPP relatif paling sehat. Beneficiary proyek IKN & infrastruktur Prabowo."
            },
            "🏗️ Swasta Konstruksi": {
                "tickers": ["TOTL.JK", "NRCA.JK", "WEGE.JK", "IDPR.JK", "PBSA.JK", "ACST.JK"],
                "info": "Konstruksi swasta lebih efisien. TOTL & NRCA konsisten profitabel. Order book terus tumbuh."
            },
        }
    },

    "media": {
        "title": "📺 SEKTOR MEDIA & HIBURAN IDX",
        "description": "Televisi, digital media, dan entertainment",
        "groups": {
            "📺 TV & Broadcasting": {
                "tickers": ["MNCN.JK", "SCMA.JK", "BMTR.JK", "RCTI.JK"],
                "info": "MNCN MNC Media & SCMA SCTV/Indosiar bersaing. Tantangan dari streaming tapi iklan TV masih dominan."
            },
            "💻 Digital Media": {
                "tickers": ["EMTK.JK", "IRSX.JK", "KBLV.JK"],
                "info": "EMTK Elang Mahkota kuasai Vidio. IRSX transformasi ke AI & media commerce. Era konten digital terus tumbuh."
            },
            "🎬 Film & Entertainment": {
                "tickers": ["FILM.JK"],
                "info": "MD Pictures produser film terbesar. Film Indonesia makin mendunia. Penonton bioskop recovery kuat."
            },
        }
    },

}


def get_sector_info_message(sector_name: str) -> str:
    """Format pesan info sektor untuk Telegram."""
    sector_name = sector_name.lower().strip()

    if sector_name not in SECTOR_INFO:
        available = ", ".join(SECTOR_INFO.keys())
        return f"❌ Sektor <b>{sector_name}</b> tidak ditemukan.\n\nTersedia: {available}"

    data   = SECTOR_INFO[sector_name]
    title  = data["title"]
    desc   = data["description"]
    groups = data["groups"]

    lines = [
        f"<b>{title}</b>",
        f"<i>{desc}</i>",
        "",
    ]

    for group_name, group_data in groups.items():
        tickers = group_data["tickers"]
        info    = group_data["info"]
        ticker_str = " | ".join([t.replace(".JK", "") for t in tickers])

        lines += [
            f"─────────────────────────",
            f"{group_name}",
            f"📌 <code>{ticker_str}</code>",
            f"💬 <i>{info}</i>",
            "",
        ]

    total_tickers = sum(len(g["tickers"]) for g in groups.values())
    lines += [
        f"─────────────────────────",
        f"Total: <b>{total_tickers} emiten</b> di sektor ini",
        f"Gunakan /sektor {sector_name} untuk scan breakout",
    ]

    return "\n".join(lines)


def get_all_sectors_list() -> str:
    """Format daftar semua sektor."""
    lines = [
        "📂 <b>DAFTAR SEKTOR TERSEDIA</b>",
        "",
    ]
    for key, data in SECTOR_INFO.items():
        title = data["title"]
        total = sum(len(g["tickers"]) for g in data["groups"].values())
        lines.append(f"• /info {key} — {title} ({total} emiten)")

    lines += [
        "",
        "<i>Ketik /info nama_sektor untuk detail emiten</i>",
        "<i>Ketik /sektor nama_sektor untuk scan breakout</i>",
    ]
    return "\n".join(lines)
