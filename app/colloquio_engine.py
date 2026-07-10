"""Contenuti informativi statici per il Modulo 3 (colloquio).

Il feedback sulle risposte del colloquio è ora generato dall'AI in una
conversazione reale (vedi app/ai_assistant.py e app/routes/colloquio.py),
non più da regole euristiche locali.
"""

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
