"""Motore a regole deterministico per il piano fisico (Modulo 1).

Non usa AI generativa: la progressione è calcolata da soglie e formule fisse
a partire dai dati raccolti in onboarding. I valori soglia sono indicativi
di riferimento generale (non i valori ufficiali di un bando specifico) e
vanno sempre confrontati con la tabella del bando scelto.
"""

from datetime import date

ESERCIZI = {
    "piegamenti": dict(nome="Piegamenti sulle braccia (push-up)", gruppo="Forza - petto/tricipiti", varianti="bodyweight"),
    "trazioni": dict(nome="Trazioni alla sbarra (pull-up)", gruppo="Forza - dorso/bicipiti", varianti="bodyweight/palestra"),
    "addominali": dict(nome="Crunch / sollevamento ginocchia", gruppo="Core", varianti="bodyweight"),
    "squat": dict(nome="Squat a corpo libero o con sovraccarico", gruppo="Forza - gambe", varianti="bodyweight/palestra"),
    "corsa_continua": dict(nome="Corsa continua a ritmo costante", gruppo="Resistenza aerobica", varianti="esterno/tapis roulant"),
    "corsa_intervalli": dict(nome="Ripetute / interval training", gruppo="Resistenza anaerobica-aerobica", varianti="esterno/pista"),
    "mobilita": dict(nome="Mobilità articolare e stretching", gruppo="Recupero", varianti="bodyweight"),
}

# Soglie indicative generali di livello (NON ufficiali di un bando specifico).
SOGLIE_LIVELLO = {
    "piegamenti": {"principiante": 15, "intermedio": 30, "avanzato": 45},
    "trazioni": {"principiante": 2, "intermedio": 6, "avanzato": 12},
    "corsa_2000m_sec": {"principiante": 660, "intermedio": 570, "avanzato": 480},  # 11', 9'30, 8'
}


def classifica_livello(profile):
    punteggi = []
    piegamenti = profile["piegamenti"] or 0
    trazioni = profile["trazioni"] or 0

    for soglia_nome, valore in (("piegamenti", piegamenti), ("trazioni", trazioni)):
        soglie = SOGLIE_LIVELLO[soglia_nome]
        if valore >= soglie["avanzato"]:
            punteggi.append(3)
        elif valore >= soglie["intermedio"]:
            punteggi.append(2)
        else:
            punteggi.append(1)

    if profile["corsa_distanza"] and profile["corsa_tempo_sec"]:
        tempo_normalizzato = profile["corsa_tempo_sec"] * (2000 / profile["corsa_distanza"])
        soglie = SOGLIE_LIVELLO["corsa_2000m_sec"]
        if tempo_normalizzato <= soglie["avanzato"]:
            punteggi.append(3)
        elif tempo_normalizzato <= soglie["intermedio"]:
            punteggi.append(2)
        else:
            punteggi.append(1)

    media = sum(punteggi) / len(punteggi) if punteggi else 1
    if media >= 2.5:
        return "avanzato"
    if media >= 1.5:
        return "intermedio"
    return "principiante"


# Durata di piano di default per livello: chi parte già in forma ha bisogno
# di meno tempo per arrivare pronto, chi parte da zero ne ha bisogno di più.
# Usata solo quando l'utente non indica una propria preferenza di durata.
SETTIMANE_DEFAULT_PER_LIVELLO = {"principiante": 12, "intermedio": 8, "avanzato": 6}


def settimane_disponibili(data_scadenza_iso, livello=None, settimane_preferite=None):
    """Calcola la durata del piano combinando tre fattori:
    - il tempo che l'utente stesso ritiene di aver bisogno (se indicato)
    - altrimenti una stima di default in base al livello di partenza individuale
    - il tempo realmente disponibile prima della scadenza del bando (se nota), che
      fa comunque da tetto massimo: non si può allenarsi più a lungo di quanto manchi.
    """
    entro_scadenza = None
    if data_scadenza_iso:
        try:
            scadenza = date.fromisoformat(data_scadenza_iso)
            giorni = (scadenza - date.today()).days
            if giorni > 0:
                entro_scadenza = giorni // 7
        except ValueError:
            pass

    if settimane_preferite:
        desiderate = max(2, min(24, settimane_preferite))
    else:
        desiderate = SETTIMANE_DEFAULT_PER_LIVELLO.get(livello, 8)

    if entro_scadenza:
        return max(4, min(entro_scadenza, desiderate, 16))
    return max(4, min(desiderate, 20))


def settimane_rimanenti(data_scadenza_iso):
    """Settimane reali rimanenti fino alla scadenza, senza il clamp usato per
    generare il piano: per uso puramente informativo in UI."""
    if not data_scadenza_iso:
        return None
    try:
        scadenza = date.fromisoformat(data_scadenza_iso)
    except ValueError:
        return None
    giorni = (scadenza - date.today()).days
    return giorni // 7 if giorni > 0 else None


STRUTTURA_GIORNI = {
    3: ["forza", "corsa", "forza_corsa"],
    4: ["forza", "corsa", "forza", "corsa_intervalli"],
    5: ["forza", "corsa", "forza", "corsa_intervalli", "mobilita"],
    6: ["forza", "corsa", "forza", "corsa_intervalli", "forza_corsa", "mobilita"],
}


def _volume_base(livello):
    return {
        "principiante": dict(piegamenti=8, trazioni=1, addominali=15, squat=10, corsa_min=12),
        "intermedio": dict(piegamenti=18, trazioni=4, addominali=25, squat=20, corsa_min=20),
        "avanzato": dict(piegamenti=30, trazioni=8, addominali=35, squat=30, corsa_min=28),
    }[livello]


def genera_piano(profile, data_scadenza_iso=None):
    livello = classifica_livello(profile)
    settimane_preferite = profile["settimane_preferite"] if "settimane_preferite" in profile.keys() else None
    n_settimane = settimane_disponibili(data_scadenza_iso, livello=livello, settimane_preferite=settimane_preferite)
    giorni_sett = profile["giorni_settimana"] or 3
    giorni_sett = min(6, max(3, giorni_sett))
    struttura = STRUTTURA_GIORNI[giorni_sett]
    base = _volume_base(livello)

    settimane = []
    for w in range(1, n_settimane + 1):
        is_deload = (w % 4 == 0) and w != n_settimane
        is_test_finale = w == n_settimane
        fattore_progressione = 1 + 0.06 * (w - 1)
        if is_deload:
            fattore_progressione *= 0.6

        giorni = []
        for tipo in struttura:
            if is_test_finale:
                sessione = dict(
                    tipo="Test di verifica / simulazione prova fisica",
                    esercizi=[
                        f"Piegamenti: massimo ripetizioni in 1 minuto (baseline: {base['piegamenti']})",
                        f"Trazioni: massimo ripetizioni (baseline: {base['trazioni']})",
                        "Corsa alla distanza ufficiale del bando scelto, a ritmo di gara",
                    ],
                )
            elif tipo == "forza":
                sessione = dict(
                    tipo="Forza",
                    esercizi=[
                        f"{ESERCIZI['piegamenti']['nome']}: {round(base['piegamenti'] * fattore_progressione)} rip. totali (3-4 serie)",
                        f"{ESERCIZI['trazioni']['nome']}: {max(1, round(base['trazioni'] * fattore_progressione))} rip. totali (3-4 serie)",
                        f"{ESERCIZI['squat']['nome']}: {round(base['squat'] * fattore_progressione)} rip. totali",
                        f"{ESERCIZI['addominali']['nome']}: {round(base['addominali'] * fattore_progressione)} rip. totali",
                    ],
                )
            elif tipo == "corsa":
                sessione = dict(
                    tipo="Resistenza",
                    esercizi=[f"{ESERCIZI['corsa_continua']['nome']}: {round(base['corsa_min'] * fattore_progressione)} minuti a ritmo costante"],
                )
            elif tipo == "corsa_intervalli":
                sessione = dict(
                    tipo="Resistenza (intervalli)",
                    esercizi=[f"{ESERCIZI['corsa_intervalli']['nome']}: 6-8 ripetute da 400m con recupero 2 min"],
                )
            elif tipo == "forza_corsa":
                sessione = dict(
                    tipo="Misto forza + corsa",
                    esercizi=[
                        f"{ESERCIZI['piegamenti']['nome']}: {round(base['piegamenti'] * fattore_progressione * 0.6)} rip.",
                        f"{ESERCIZI['corsa_continua']['nome']}: {round(base['corsa_min'] * fattore_progressione * 0.6)} minuti",
                    ],
                )
            else:
                sessione = dict(tipo="Mobilità e recupero", esercizi=[ESERCIZI["mobilita"]["nome"]])
            giorni.append(sessione)

        settimane.append(dict(
            numero=w,
            deload=is_deload,
            test_finale=is_test_finale,
            giorni=giorni,
        ))

    return dict(livello=livello, n_settimane=n_settimane, giorni_a_settimana=giorni_sett, settimane=settimane)
