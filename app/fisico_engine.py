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

# Soglie di riferimento per corpo, ISPIRATE ai valori tipici delle edizioni
# recenti dei rispettivi concorsi. Variano per edizione, sesso ed età: sono
# valori orientativi per capire il proprio divario, non i minimi ufficiali —
# quelli fanno fede solo sul bando specifico.
# Soglie con valori distinti uomo/donna (i bandi reali differenziano per sesso
# e talvolta per età): valori tipici delle edizioni recenti, orientativi.
SOGLIE_PER_CORPO = {
    "Carabinieri": dict(
        etichetta="Allievi Carabinieri",
        prove=[
            dict(nome="Corsa 1000 m", tipo="corsa", distanza=1000, tempo_max_sec=dict(M=240, F=280)),
            dict(nome="Piegamenti sulle braccia", tipo="piegamenti", minimo=dict(M=15, F=11)),
        ],
    ),
    "Guardia di Finanza": dict(
        etichetta="Concorsi Guardia di Finanza",
        prove=[
            dict(nome="Corsa 1000 m", tipo="corsa", distanza=1000, tempo_max_sec=dict(M=235, F=275)),
            dict(nome="Piegamenti sulle braccia", tipo="piegamenti", minimo=dict(M=15, F=10)),
        ],
    ),
    "Esercito/Marina/Aeronautica": dict(
        etichetta="VFI / prove Forze Armate",
        prove=[
            dict(nome="Corsa 2000 m", tipo="corsa", distanza=2000, tempo_max_sec=dict(M=630, F=750)),
            dict(nome="Piegamenti sulle braccia", tipo="piegamenti", minimo=dict(M=12, F=8)),
            dict(nome="Trazioni alla sbarra", tipo="trazioni", minimo=dict(M=3, F=1)),
        ],
    ),
}


def confronto_soglie(profile, corpo_tag):
    """Confronta i valori dell'utente con le soglie tipiche del suo corpo,
    differenziate per sesso quando indicato (default: valori uomo).

    Ritorna una lista di dict con: prova, richiesto, tuo, ok (bool o None se
    manca il dato), gap (testo leggibile).
    """
    config = SOGLIE_PER_CORPO.get(corpo_tag)
    if not config:
        return None

    sesso = "F" if ("sesso" in profile.keys() and profile["sesso"] == "F") else "M"

    def fmt_tempo(sec):
        return f"{sec // 60}'{sec % 60:02d}\""

    righe = []
    for prova in config["prove"]:
        if prova["tipo"] == "corsa":
            tempo_max = prova["tempo_max_sec"][sesso]
            richiesto = f"≤ {fmt_tempo(tempo_max)}"
            if profile["corsa_distanza"] and profile["corsa_tempo_sec"]:
                # Normalizzazione proporzionale alla distanza della prova:
                # approssimata (il ritmo reale non scala linearmente).
                tempo_norm = round(profile["corsa_tempo_sec"] * (prova["distanza"] / profile["corsa_distanza"]))
                ok = tempo_norm <= tempo_max
                gap = tempo_norm - tempo_max
                righe.append(dict(
                    prova=prova["nome"], richiesto=richiesto,
                    tuo=f"~{fmt_tempo(tempo_norm)} (stimato dal tuo test)",
                    ok=ok,
                    gap=("Nei limiti" if ok else f"Ti mancano circa {gap} secondi"),
                ))
            else:
                righe.append(dict(prova=prova["nome"], richiesto=richiesto, tuo="dato mancante", ok=None, gap="Registra un test per confrontarti"))
        else:
            campo = prova["tipo"]
            minimo = prova["minimo"][sesso]
            valore = profile[campo]
            richiesto = f"≥ {minimo}"
            if valore is not None:
                ok = valore >= minimo
                righe.append(dict(
                    prova=prova["nome"], richiesto=richiesto, tuo=str(valore), ok=ok,
                    gap=("Nei limiti" if ok else f"Te ne mancano {minimo - valore}"),
                ))
            else:
                righe.append(dict(prova=prova["nome"], richiesto=richiesto, tuo="dato mancante", ok=None, gap="Registra un test per confrontarti"))

    etichetta_sesso = "valori tipici donna" if sesso == "F" else "valori tipici uomo"
    return dict(etichetta=f"{config['etichetta']} ({etichetta_sesso})", righe=righe)


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


RISCALDAMENTO = "Riscaldamento: 8-10 minuti di corsa leggera + mobilità articolare (mai saltarlo)"
DEFATICAMENTO = "Defaticamento: 5 minuti di camminata + stretching dei muscoli usati"

# Riposo consigliato tra gli esercizi, in secondi, per tipo di sessione.
RIPOSO_PER_TIPO = {
    "Forza": 90,
    "Misto forza + corsa": 75,
    "Resistenza": 60,
    "Resistenza (intervalli)": 60,
    "Mobilità e recupero": 45,
}


def _nome_trazioni(contesto):
    """Chi non ha una sbarra (corpo libero/esterno senza attrezzi) riceve una
    variante equivalente invece di un esercizio impossibile da eseguire."""
    if contesto in ("corpo_libero",):
        return ("Trazioni orizzontali (australiane) con tavolo robusto o sbarra bassa "
                "— se hai accesso a una sbarra, trazioni classiche")
    return ESERCIZI["trazioni"]["nome"]


def dati_test_mancanti(profile):
    """True se mancano i dati di partenza (o l'utente ha chiesto il test guidato)."""
    non_lo_so = bool(profile["non_lo_so"]) if "non_lo_so" in profile.keys() else False
    mancano = (
        profile["piegamenti"] is None
        or profile["trazioni"] is None
        or profile["corsa_tempo_sec"] is None
    )
    return non_lo_so or mancano


def _settimana_test_guidato(giorni_sett, contesto):
    """Prima settimana per chi parte senza dati: test guidati per misurare la
    baseline, da registrare nella pagina 'Registra un test'."""
    trazioni_nome = _nome_trazioni(contesto)
    sessioni = [
        dict(tipo="Test guidato: forza superiore", esercizi=[
            RISCALDAMENTO,
            "Piegamenti sulle braccia: massimo di ripetizioni consecutive con tecnica corretta (fermati quando la forma cede)",
            f"{trazioni_nome}: massimo di ripetizioni consecutive",
            DEFATICAMENTO,
        ]),
        dict(tipo="Test guidato: corsa cronometrata", esercizi=[
            RISCALDAMENTO,
            "Corsa 2000 m cronometrata a sforzo massimo sostenibile (usa un'app GPS o una pista)",
            DEFATICAMENTO,
        ]),
        dict(tipo="Test guidato: gambe e core", esercizi=[
            RISCALDAMENTO,
            "Squat a corpo libero: massimo di ripetizioni in 2 minuti",
            "Plank: tenuta massima in secondi",
            DEFATICAMENTO,
        ]),
    ]
    return sessioni[:max(3, min(giorni_sett, 3))] + (
        [dict(tipo="Mobilità e recupero", esercizi=[ESERCIZI["mobilita"]["nome"]])] * max(0, giorni_sett - 3)
    )


def genera_piano(profile, data_scadenza_iso=None):
    livello = classifica_livello(profile)
    settimane_preferite = profile["settimane_preferite"] if "settimane_preferite" in profile.keys() else None
    n_settimane = settimane_disponibili(data_scadenza_iso, livello=livello, settimane_preferite=settimane_preferite)
    giorni_sett = profile["giorni_settimana"] or 3
    giorni_sett = min(6, max(3, giorni_sett))
    struttura = STRUTTURA_GIORNI[giorni_sett]
    base = _volume_base(livello)
    contesto = profile["contesto"] if "contesto" in profile.keys() else None
    trazioni_nome = _nome_trazioni(contesto)
    test_iniziale = dati_test_mancanti(profile)

    settimane = []
    for w in range(1, n_settimane + 1):
        is_test_iniziale = test_iniziale and w == 1
        is_deload = (w % 4 == 0) and w != n_settimane and not is_test_iniziale
        is_test_finale = w == n_settimane
        fattore_progressione = 1 + 0.06 * (w - 1)
        if is_deload:
            fattore_progressione *= 0.6

        if is_test_iniziale:
            giorni = _settimana_test_guidato(giorni_sett, contesto)
        else:
            giorni = []
            for tipo in struttura:
                if is_test_finale:
                    sessione = dict(
                        tipo="Test di verifica / simulazione prova fisica",
                        esercizi=[
                            RISCALDAMENTO,
                            f"Piegamenti: massimo ripetizioni in 1 minuto (baseline: {base['piegamenti']})",
                            f"Trazioni: massimo ripetizioni (baseline: {base['trazioni']})",
                            "Corsa alla distanza ufficiale del bando scelto, a ritmo di gara",
                            "Registra i risultati nella pagina 'Registra un test' per ricalibrare il piano",
                        ],
                    )
                elif tipo == "forza":
                    sessione = dict(
                        tipo="Forza",
                        esercizi=[
                            RISCALDAMENTO,
                            f"{ESERCIZI['piegamenti']['nome']}: {round(base['piegamenti'] * fattore_progressione)} rip. totali (3-4 serie)",
                            f"{trazioni_nome}: {max(1, round(base['trazioni'] * fattore_progressione))} rip. totali (3-4 serie)",
                            f"{ESERCIZI['squat']['nome']}: {round(base['squat'] * fattore_progressione)} rip. totali",
                            f"{ESERCIZI['addominali']['nome']}: {round(base['addominali'] * fattore_progressione)} rip. totali",
                            DEFATICAMENTO,
                        ],
                    )
                elif tipo == "corsa":
                    sessione = dict(
                        tipo="Resistenza",
                        esercizi=[
                            RISCALDAMENTO,
                            f"{ESERCIZI['corsa_continua']['nome']}: {round(base['corsa_min'] * fattore_progressione)} minuti a ritmo costante",
                            DEFATICAMENTO,
                        ],
                    )
                elif tipo == "corsa_intervalli":
                    sessione = dict(
                        tipo="Resistenza (intervalli)",
                        esercizi=[
                            RISCALDAMENTO,
                            f"{ESERCIZI['corsa_intervalli']['nome']}: 6-8 ripetute da 400m con recupero 2 min",
                            DEFATICAMENTO,
                        ],
                    )
                elif tipo == "forza_corsa":
                    sessione = dict(
                        tipo="Misto forza + corsa",
                        esercizi=[
                            RISCALDAMENTO,
                            f"{ESERCIZI['piegamenti']['nome']}: {round(base['piegamenti'] * fattore_progressione * 0.6)} rip.",
                            f"{ESERCIZI['corsa_continua']['nome']}: {round(base['corsa_min'] * fattore_progressione * 0.6)} minuti",
                            DEFATICAMENTO,
                        ],
                    )
                else:
                    sessione = dict(tipo="Mobilità e recupero", esercizi=[ESERCIZI["mobilita"]["nome"]])
                giorni.append(sessione)

        for sessione in giorni:
            sessione["riposo_sec"] = RIPOSO_PER_TIPO.get(sessione["tipo"], 60 if "Test" in sessione["tipo"] else 90)

        settimane.append(dict(
            numero=w,
            deload=is_deload,
            test_finale=is_test_finale,
            test_iniziale=is_test_iniziale,
            giorni=giorni,
        ))

    return dict(
        livello=livello, n_settimane=n_settimane, giorni_a_settimana=giorni_sett,
        settimane=settimane, test_iniziale=test_iniziale,
    )
