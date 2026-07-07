"""Feedback euristico (regole, non AI generativa) per le risposte motivazionali.

Deliberatamente NON assegna punteggi numerici: fornisce solo osservazioni
qualitative su struttura e chiarezza, come indicato nel disclaimer del
Modulo 3 (non è un test psicologico, non sostituisce lo psicologo militare).
"""

CLICHE = [
    "fin da piccolo", "fin da bambino", "amo la patria", "servire il mio paese",
    "sempre stato il mio sogno", "onore e disciplina", "sono nato per questo",
]

PAROLE_CONCRETEZZA = [
    "quando", "esperienza", "ho fatto", "ho svolto", "durante", "esempio",
    "in particolare", "mesi", "anni", "allenamento", "corso", "lavoro", "progetto",
]

DOMANDE = [
    "Perché vuoi entrare nelle Forze Armate / nell'Arma dei Carabinieri?",
    "Racconta un episodio in cui hai dovuto rispettare una regola che non condividevi.",
    "Come reagisci sotto pressione o in una situazione di stress improvviso?",
    "Descrivi un'esperienza di lavoro in squadra e il tuo ruolo in quel contesto.",
    "Quali pensi siano i tuoi punti di forza e i tuoi limiti rispetto alla vita militare?",
]

# Contenuti informativi generali sulla gestione dell'ansia da colloquio: solo
# indicazioni pratiche di preparazione, non consigli terapeutici. Il rimando
# a un professionista in caso di ansia persistente è deliberato, non un
# dettaglio decorativo.
SEZIONI_ANSIA = [
    dict(
        titolo="Prima del colloquio",
        punti=[
            "Rileggi la tua domanda e il percorso che hai fatto per arrivarci: sapere 'perché sei lì' riduce l'incertezza.",
            "Prepara in anticipo 2-3 episodi concreti della tua vita che puoi usare per rispondere a domande diverse.",
            "Dormi a sufficienza la notte prima: il sonno incide sulla lucidità più di un'ultima ora di ripasso.",
            "Arriva con largo anticipo: la fretta è una delle cause più comuni di ansia acuta pre-colloquio.",
        ],
    ),
    dict(
        titolo="Tecniche di respirazione rapide",
        punti=[
            "Respirazione 4-7-8: inspira contando fino a 4, trattieni fino a 7, espira fino a 8. Ripeti 3-4 volte prima di entrare.",
            "Respirazione quadrata (box breathing): inspira, trattieni, espira, trattieni, ciascuna fase per 4 secondi.",
            "Sono tecniche di rilassamento generali usate anche in ambito sportivo, non un trattamento clinico dell'ansia.",
        ],
    ),
    dict(
        titolo="Come strutturare una risposta sotto stress",
        punti=[
            "Metodo S-C-A-R: Situazione (contesto), Compito (cosa dovevi fare), Azione (cosa hai fatto tu), Risultato (cosa è successo).",
            "Se ti blocchi, va bene dire 'mi lasci un attimo per riordinare le idee': una breve pausa è normale e non penalizzante.",
            "Rispondi a quello che ti è stato chiesto per primo, poi aggiungi dettagli: evita di divagare per riempire il silenzio.",
        ],
    ),
    dict(
        titolo="Cosa aspettarsi il giorno della selezione psicoattitudinale",
        punti=[
            "Di solito comprende test scritti standardizzati e uno o più colloqui individuali con personale specializzato.",
            "Non esistono 'risposte giuste' universali: l'obiettivo è valutare coerenza, stabilità e consapevolezza di sé, non recitare una parte.",
            "È normale sentirsi valutati e un po' in ansia: fa parte dell'esperienza, non è un segnale che qualcosa non va.",
        ],
    ),
    dict(
        titolo="Quando l'ansia è più di una tensione normale",
        punti=[
            "Se l'ansia da prestazione è persistente, ti impedisce di dormire per settimane o si accompagna ad attacchi di panico, "
            "parlarne con un medico o uno psicologo è il passo giusto, non un segno di debolezza.",
            "Questa pagina offre solo indicazioni pratiche generali: non è un percorso terapeutico e non sostituisce un professionista.",
        ],
    ),
]


def analizza_risposta(testo):
    testo_lower = testo.lower()
    parole = testo.split()
    n_parole = len(parole)

    osservazioni = []

    if n_parole < 20:
        osservazioni.append("La risposta è molto breve: prova ad ampliarla con un esempio concreto.")
    elif n_parole > 180:
        osservazioni.append("La risposta è piuttosto lunga: in un colloquio reale punta a essere più sintetico e diretto.")
    else:
        osservazioni.append("La lunghezza della risposta è adeguata a un colloquio orale.")

    cliche_trovati = [c for c in CLICHE if c in testo_lower]
    if cliche_trovati:
        osservazioni.append(
            "Contiene frasi molto generiche/di circostanza (" + ", ".join(cliche_trovati) + "): "
            "prova a sostituirle con qualcosa di personale e verificabile."
        )

    ha_concretezza = any(p in testo_lower for p in PAROLE_CONCRETEZZA)
    if ha_concretezza:
        osservazioni.append("Bene: la risposta include riferimenti a esperienze o momenti concreti.")
    else:
        osservazioni.append("Manca un riferimento a un'esperienza concreta o a un episodio specifico: aggiungine uno.")

    usa_prima_persona = any(p in testo_lower.split() for p in ["io", "mi", "ho", "sono"])
    if not usa_prima_persona:
        osservazioni.append("Prova a parlare più in prima persona, di te stesso e delle tue esperienze dirette.")

    return dict(n_parole=n_parole, osservazioni=osservazioni, cliche_trovati=cliche_trovati)
