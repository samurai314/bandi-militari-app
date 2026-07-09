"""Icone SVG minimali (stroke, currentColor) per gli esercizi e i tipi di sessione.

Sono disegni originali molto semplici (silhouette stilizzate), non asset di
terzi: servono a dare un riferimento visivo rapido senza dover ospitare
foto/video esterni.
"""

_ICONE = {
    "piegamenti": """<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="10" cy="16" r="3.2"/>
        <path d="M13 18 L38 30"/>
        <path d="M20 21.5 L16 34"/>
        <path d="M31 26.5 L34 38"/>
        <path d="M16 34 L10 38"/>
        <path d="M34 38 L40 34"/>
    </svg>""",
    "trazioni": """<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M6 10 H42"/>
        <circle cx="24" cy="18" r="3.2"/>
        <path d="M18 11 L24 21 L30 11"/>
        <path d="M24 21 V32"/>
        <path d="M24 32 L18 42"/>
        <path d="M24 32 L30 42"/>
    </svg>""",
    "squat": """<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="24" cy="10" r="3.2"/>
        <path d="M14 20 H34"/>
        <path d="M24 13 V24"/>
        <path d="M24 24 L16 30 L18 42"/>
        <path d="M24 24 L32 30 L30 42"/>
    </svg>""",
    "addominali": """<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M6 34 H16"/>
        <circle cx="24" cy="22" r="3.2"/>
        <path d="M20 26 Q14 34 8 34"/>
        <path d="M20 26 L30 30"/>
        <path d="M30 30 L28 40"/>
        <path d="M30 30 L38 34"/>
    </svg>""",
    "corsa_continua": """<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="28" cy="9" r="3.2"/>
        <path d="M25 12 L18 22 L26 24"/>
        <path d="M26 24 L20 34"/>
        <path d="M26 24 L34 30 L38 26"/>
        <path d="M18 22 L9 18"/>
        <path d="M20 34 L12 40"/>
        <path d="M20 34 L26 42"/>
    </svg>""",
    "corsa_intervalli": """<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="20" cy="9" r="3.2"/>
        <path d="M17 12 L10 22 L18 24"/>
        <path d="M18 24 L12 34"/>
        <path d="M18 24 L26 30 L30 26"/>
        <path d="M10 22 L2 18"/>
        <path d="M34 10 L28 22 L36 20 L30 34" stroke-width="2"/>
    </svg>""",
    "mobilita": """<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="24" cy="9" r="3.2"/>
        <path d="M24 12 V26"/>
        <path d="M24 15 L12 8"/>
        <path d="M24 15 L36 8"/>
        <path d="M24 26 L16 40"/>
        <path d="M24 26 L32 40"/>
    </svg>""",
    "test": """<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="24" cy="26" r="14"/>
        <path d="M24 26 V16"/>
        <path d="M24 26 L31 30"/>
        <path d="M19 4 H29"/>
        <path d="M24 4 V8"/>
    </svg>""",
}

_KEYWORD_MAP = [
    ("piegamenti", "piegamenti"),
    ("trazioni", "trazioni"),
    ("squat", "squat"),
    ("crunch", "addominali"),
    ("sollevamento ginocchia", "addominali"),
    ("ripetute", "corsa_intervalli"),
    ("interval", "corsa_intervalli"),
    ("corsa continua", "corsa_continua"),
    ("mobilità", "mobilita"),
    ("stretching", "mobilita"),
    ("test", "test"),
]


def icona_per_esercizio(testo):
    testo_lower = (testo or "").lower()
    for parola, chiave in _KEYWORD_MAP:
        if parola in testo_lower:
            return _ICONE[chiave]
    return _ICONE["mobilita"]


# Video dimostrativi reali (YouTube), scelti per chiarezza della tecnica e
# autorevolezza del canale. Sono contenuti di terzi incorporati via embed
# standard, non file ospitati da questa app: se un video venisse rimosso
# andrebbe sostituito qui.
_VIDEO_ID = {
    "piegamenti": "b0Xhc1aN5jQ",
    "trazioni": "dArMGj22n44",
    "squat": "MBgZNiN98AE",
    "addominali": "pe24qldX2Y4",
    "corsa_continua": "qirA0ZAFiAM",
    "corsa_intervalli": "qirA0ZAFiAM",
    "mobilita": "eJQMB5qfNXw",
    "test": None,
}


def video_per_esercizio(testo):
    testo_lower = (testo or "").lower()
    for parola, chiave in _KEYWORD_MAP:
        if parola in testo_lower:
            return _VIDEO_ID.get(chiave)
    return _VIDEO_ID["mobilita"]
