"""Ricerca per parole chiave sui testi dei bandi indicizzati (Modulo 5, prototipo).

Non è un agente RAG con un vero LLM: è un motore di retrieval per
sovrapposizione di parole chiave. Ogni risultato riporta sempre la fonte
e la data, in linea con il disclaimer del blueprint originale.
"""

import re

STOPWORDS = {
    "il", "lo", "la", "i", "gli", "le", "di", "a", "da", "in", "con", "su", "per",
    "tra", "fra", "un", "uno", "una", "e", "o", "che", "chi", "come", "quando",
    "dove", "quale", "quali", "sono", "è", "cosa", "posso", "devo", "mi", "ci",
    "del", "della", "dei", "delle", "al", "allo", "alla", "ai", "agli", "alle",
}


def _tokenize(testo):
    parole = re.findall(r"[a-zàèéìòù0-9]+", testo.lower())
    return [p for p in parole if p not in STOPWORDS and len(p) > 2]


def cerca(bandi_rows, domanda, top_n=3):
    keywords = _tokenize(domanda)
    if not keywords:
        return []

    risultati = []
    for b in bandi_rows:
        corpus = f"{b['titolo']} {b['descrizione']} {b['testo_indicizzato']}".lower()
        score = sum(corpus.count(k) for k in keywords)
        if score > 0:
            risultati.append((score, b))

    risultati.sort(key=lambda x: x[0], reverse=True)
    return [b for _, b in risultati[:top_n]]
