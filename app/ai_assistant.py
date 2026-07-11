"""Integrazione reale con Claude (Anthropic): chat streaming multi-turno per
bandi, coach fisico e colloquio.

Il corpus dei bandi è piccolo (poche decine di voci), quindi invece di un
retrieval per embedding passiamo l'intero corpus indicizzato come contesto:
è un RAG "a corpus intero", non serve altro finché il database resta di
queste dimensioni.

Per i bandi non indicizzati (o per domande generali sulla vita militare)
l'assistente usa il tool di ricerca web nativo di Claude — eseguito lato
server da Anthropic stessa, non dal nostro backend, quindi non soggetto a
eventuali restrizioni di rete dell'hosting.
"""

import anthropic

MODEL = "claude-haiku-4-5-20251001"

# Numero massimo di messaggi (utente+assistente) inviati come cronologia ad
# ogni richiesta: oltre questa soglia teniamo solo i più recenti, per evitare
# che conversazioni molto lunghe facciano crescere il costo indefinitamente.
MAX_MESSAGGI_STORICO = 30

WEB_SEARCH_TOOL = {"type": "web_search_20250305", "name": "web_search", "max_uses": 3}

SYSTEM_PROMPT_BANDI_CHAT = """Sei l'assistente conversazionale di un'app di preparazione ai concorsi militari
italiani. Per fatti concreti su un bando (date, requisiti, numero di posti) usa PRIMA i testi dei bandi
indicizzati forniti nel contesto qui sotto, e cita sempre il titolo del bando e la fonte quando rispondi
con un dato preciso preso da lì: non inventare mai date, requisiti o numeri di posti.

Se ti viene chiesto di un bando che NON è nel contesto fornito, usa lo strumento di ricerca web per
cercarlo: quando lo fai, cita sempre la fonte trovata (nome del sito e se possibile l'URL) e ricorda
comunque all'utente di verificare il testo integrale sul sito ufficiale o sulla Gazzetta Ufficiale prima
di presentare domanda.

Per domande generali sulla vita militare, la carriera, o su come funzionano le prove di selezione in
generale (non un dato specifico di un bando) puoi rispondere anche con conoscenza generale o cercando
sul web se utile, ma dichiara sempre chiaramente che è un'informazione generale/indicativa, non una
garanzia ufficiale.

Questa è una conversazione a più turni: puoi fare riferimento a quanto detto prima. Rispondi in italiano,
in modo naturale e colloquiale ma preciso, senza markdown pesante."""

SYSTEM_PROMPT_COACH_FISICO = """Sei il coach virtuale del piano fisico di un'app di preparazione ai concorsi
militari italiani. Conosci il piano di allenamento dell'utente, le sessioni che ha completato, la sua
streak giornaliera: usa questi dati (forniti nel contesto) per dare consigli mirati, motivazione e
risposte a domande su come eseguire gli esercizi o adattare il carico.
Non sei un preparatore atletico o un medico reale: se l'utente segnala dolore, infortuni o dubbi
medici, invitalo sempre a consultare un professionista invece di dare indicazioni cliniche.
Rispondi in italiano, tono diretto e incoraggiante, conversazionale (questa è una chat a più turni)."""

SYSTEM_PROMPT_COLLOQUIO_CHAT = """Sei un intervistatore che simula, in modo realistico, un colloquio
motivazionale per un concorso militare italiano (non la selezione psicoattitudinale ufficiale, che è
condotta da professionisti con strumenti diversi).

Comportati come un vero colloquio: fai UNA domanda alla volta (motivazionali, situazionali, gestione
dello stress, lavoro di squadra, valori — variale, non ripetere sempre le stesse), aspetta la risposta
del candidato, poi fai una domanda di follow-up naturale o passa al tema successivo. Tono professionale
ma non ostile, come farebbe un vero selezionatore. Se è il primo messaggio della conversazione, presentati
brevemente e fai la prima domanda.

Quando l'utente scrive esattamente "Per favore concludi il colloquio e dammi una valutazione dettagliata
di ogni mia risposta.", interrompi le domande e fornisci invece una valutazione strutturata: per OGNI
risposta data finora nella conversazione, un giudizio qualitativo breve su chiarezza, coerenza e
concretezza (es. "risposta 1: chiara ma generica, manca un esempio concreto"). Poi un breve commento
d'insieme. NON assegnare mai un punteggio numerico, non fare alcuna valutazione psicologica o clinica
della persona, non dire se "supererebbe" o meno una selezione reale.

Rispondi sempre in italiano, senza markdown pesante (niente intestazioni, al massimo elenchi puntati
semplici nella valutazione finale)."""

SYSTEM_PROMPT_RIPASSO = """Sei un tutor di preparazione ai concorsi militari italiani. Ricevi un elenco
di domande a cui lo studente ha risposto in modo sbagliato. Scrivi una mini-lezione di ripasso in
italiano che spieghi in modo chiaro e memorizzabile i concetti dietro quelle domande: raggruppa per
argomento, spiega il perché della risposta corretta e aggiungi, dove utile, un trucco mnemonico o un
collegamento che aiuti a ricordare. Concludi con 2-3 punti chiave da fissare. Massimo 350 parole,
niente markdown pesante (al massimo elenchi puntati semplici)."""

TRIGGER_VALUTAZIONE_COLLOQUIO = (
    "Per favore concludi il colloquio e dammi una valutazione dettagliata di ogni mia risposta."
)


def build_coach_context(profile, piano, sessioni_fatte, totale_sessioni, streak):
    return (
        f"Livello classificato: {piano['livello']}. Piano di {piano['n_settimane']} settimane, "
        f"{piano['giorni_a_settimana']} giorni/settimana.\n"
        f"Sessioni completate finora: {sessioni_fatte} su {totale_sessioni} totali.\n"
        f"Streak attuale: {streak['current_streak'] if streak else 0} giorni consecutivi "
        f"(record personale: {streak['longest_streak'] if streak else 0}).\n"
        f"Sport pregresso: {profile['sport'] or 'nessuno indicato'}. "
        f"Limitazioni fisiche indicate: {profile['limitazioni'] or 'nessuna'}."
    )


def stream_chat(api_key, system_prompt, messaggi, abilita_ricerca_web=False):
    """Generator che produce il testo della risposta Claude a pezzi, per lo streaming lato client.

    messaggi: lista di {"role": "user"|"assistant", "content": str}, cronologia completa
    della conversazione (senza il system prompt, passato separatamente).
    """
    if not api_key:
        yield "[Assistente AI non configurato in questo ambiente.]"
        return

    if len(messaggi) > MAX_MESSAGGI_STORICO:
        messaggi = messaggi[-MAX_MESSAGGI_STORICO:]
        # Il primo messaggio della cronologia troncata deve restare di ruolo
        # "user" (l'API richiede che la conversazione inizi con l'utente).
        while messaggi and messaggi[0]["role"] != "user":
            messaggi = messaggi[1:]

    kwargs = dict(model=MODEL, max_tokens=800, system=system_prompt, messages=messaggi)
    if abilita_ricerca_web:
        kwargs["tools"] = [WEB_SEARCH_TOOL]

    try:
        client = anthropic.Anthropic(api_key=api_key)
        with client.messages.stream(**kwargs) as stream:
            for testo in stream.text_stream:
                yield testo
    except anthropic.APIError as e:
        yield f"\n\n[Errore nel contattare l'assistente AI: {e}]"
    except Exception as e:
        yield f"\n\n[Errore imprevisto: {e}]"
