"""Integrazione reale con Claude (Anthropic) per l'agente bandi e il feedback colloquio.

Il corpus dei bandi è piccolo (poche decine di voci), quindi invece di un
retrieval per embedding passiamo l'intero corpus indicizzato come contesto:
è un RAG "a corpus intero", non serve altro finché il database resta di
queste dimensioni. Se il DB crescesse molto andrebbe introdotta una vera
ricerca vettoriale prima di questo passaggio.

Ogni chiamata è difensiva: se la chiave manca o l'API fallisce, ritorna
ok=False e il chiamante ricade sul comportamento non-AI già esistente.
"""

import anthropic

MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT_BANDI = """Sei l'assistente informativo di un'app di preparazione ai concorsi militari italiani.
Rispondi SOLO usando i testi dei bandi forniti nel contesto qui sotto: non usare conoscenza generale
o esterna su bandi militari, anche se la conosci. Se l'informazione richiesta non è presente nel
contesto fornito, dillo esplicitamente e invita l'utente a verificare sul bando ufficiale o sulla
Gazzetta Ufficiale: non inventare mai date, requisiti o numeri di posti.
Quando rispondi, cita sempre il titolo del bando e la fonte. Rispondi in italiano, in modo conciso
(massimo 120-150 parole), senza markdown pesante (evita intestazioni, usa al massimo elenchi puntati semplici)."""

SYSTEM_PROMPT_COLLOQUIO = """Sei un assistente che aiuta candidati a concorsi militari italiani a esercitarsi
con domande motivazionali in vista del colloquio/selezione psicoattitudinale.
Dai SOLO feedback qualitativo su chiarezza, struttura e concretezza della risposta (es. se è troppo
generica, se manca un esempio concreto, se la lunghezza è adeguata a un colloquio orale).
Non assegnare mai un punteggio numerico, non fare alcuna valutazione psicologica o clinica della
persona, non dire se "supererebbe" o meno una selezione reale: quella è condotta da professionisti
con strumenti diversi. Rispondi in italiano, in 3-5 punti elenco brevi, tono diretto e costruttivo."""

SYSTEM_PROMPT_BANDI_CHAT = """Sei l'assistente conversazionale di un'app di preparazione ai concorsi militari
italiani. Rispondi SOLO usando i testi dei bandi forniti nel contesto qui sotto: non usare conoscenza
generale o esterna, anche se la conosci. Se l'informazione richiesta non è nel contesto, dillo
esplicitamente e invita a verificare sul bando ufficiale o sulla Gazzetta Ufficiale: non inventare mai
date, requisiti o numeri di posti. Cita sempre il titolo del bando e la fonte quando rispondi con un
dato preciso. Questa è una conversazione a più turni: puoi fare riferimento a quanto detto prima.
Rispondi in italiano, in modo naturale e colloquiale ma preciso, senza markdown pesante."""

SYSTEM_PROMPT_COACH_FISICO = """Sei il coach virtuale del piano fisico di un'app di preparazione ai concorsi
militari italiani. Conosci il piano di allenamento dell'utente, le sessioni che ha completato, la sua
streak giornaliera: usa questi dati (forniti nel contesto) per dare consigli mirati, motivazione e
risposte a domande su come eseguire gli esercizi o adattare il carico.
Non sei un preparatore atletico o un medico reale: se l'utente segnala dolore, infortuni o dubbi
medici, invitalo sempre a consultare un professionista invece di dare indicazioni cliniche.
Rispondi in italiano, tono diretto e incoraggiante, conversazionale (questa è una chat a più turni)."""


def _build_bandi_context(bandi_rows):
    blocchi = []
    for b in bandi_rows:
        blocchi.append(
            f"### {b['titolo']}\n"
            f"Corpo: {b['corpo']} | Categoria: {b['categoria']} | Posti: {b['posti']}\n"
            f"Pubblicato: {b['data_pubblicazione'] or 'n.d.'} | Apertura: {b['data_apertura'] or 'n.d.'} | "
            f"Scadenza: {b['data_scadenza'] or 'n.d.'}{' (STIMA, non ufficiale)' if b['stimato'] else ''}\n"
            f"Descrizione: {b['descrizione']}\n"
            f"Dettagli aggiuntivi: {b['testo_indicizzato']}\n"
            f"Fonte: {b['fonte_url']} ({b['fonte_tipo']})\n"
        )
    return "\n".join(blocchi)


def ask_bandi_assistant(api_key, bandi_rows, domanda):
    if not api_key:
        return dict(ok=False, error="no_api_key")

    contesto = _build_bandi_context(bandi_rows)
    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=MODEL,
            max_tokens=500,
            system=SYSTEM_PROMPT_BANDI,
            messages=[
                {
                    "role": "user",
                    "content": f"CONTESTO (testi dei bandi indicizzati):\n{contesto}\n\nDOMANDA: {domanda}",
                }
            ],
        )
        testo = "".join(block.text for block in response.content if block.type == "text")
        return dict(ok=True, testo=testo.strip())
    except anthropic.APIError as e:
        return dict(ok=False, error=f"api_error: {e}")
    except Exception as e:
        return dict(ok=False, error=f"errore: {e}")


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


def stream_chat(api_key, system_prompt, messaggi):
    """Generator che produce il testo della risposta Claude a pezzi, per lo streaming lato client.

    messaggi: lista di {"role": "user"|"assistant", "content": str}, cronologia completa
    della conversazione (senza il system prompt, passato separatamente).
    """
    if not api_key:
        yield "[Assistente AI non configurato in questo ambiente.]"
        return

    try:
        client = anthropic.Anthropic(api_key=api_key)
        with client.messages.stream(
            model=MODEL,
            max_tokens=700,
            system=system_prompt,
            messages=messaggi,
        ) as stream:
            for testo in stream.text_stream:
                yield testo
    except anthropic.APIError as e:
        yield f"\n\n[Errore nel contattare l'assistente AI: {e}]"
    except Exception as e:
        yield f"\n\n[Errore imprevisto: {e}]"


def ai_feedback_colloquio(api_key, domanda, risposta):
    if not api_key:
        return dict(ok=False, error="no_api_key")

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=MODEL,
            max_tokens=400,
            system=SYSTEM_PROMPT_COLLOQUIO,
            messages=[
                {
                    "role": "user",
                    "content": f"DOMANDA DI COLLOQUIO: {domanda}\n\nRISPOSTA DEL CANDIDATO: {risposta}",
                }
            ],
        )
        testo = "".join(block.text for block in response.content if block.type == "text")
        return dict(ok=True, testo=testo.strip())
    except anthropic.APIError as e:
        return dict(ok=False, error=f"api_error: {e}")
    except Exception as e:
        return dict(ok=False, error=f"errore: {e}")
