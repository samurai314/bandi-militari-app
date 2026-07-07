# Dati reali raccolti da fonti ufficiali/pubbliche (luglio 2026).
# Le date di scadenza/apertura sono riportate come trovate sulle fonti citate:
# vanno sempre riverificate sul bando ufficiale integrale prima di presentare domanda.

from .db import get_db

BANDI = [
    dict(
        corpo="Interforze (Esercito, Marina, Aeronautica)",
        categoria="VFT (Volontari Ferma Triennale)",
        titolo="Concorso VFT 2026 - 3.382 posti (Esercito, Marina, Aeronautica)",
        posti="3.382 posti totali (poi rimodulati: Esercito 1.555, Marina 845, Aeronautica 732)",
        descrizione=(
            "Concorso per titoli ed esami riservato a VFI in servizio da almeno 24 mesi e a VFP1 "
            "in servizio o in congedo (fino al 31/12/2026) per l'ammissione alla ferma triennale (VFT) "
            "nelle tre Forze Armate."
        ),
        testo_indicizzato=(
            "Concorso VFT 2026 volontari ferma triennale Esercito Marina Aeronautica riservato VFI "
            "VFP1 servizio congedo titoli esami rimodulazione posti Corpo Equipaggi Militari Marittimi "
            "CEMM Capitanerie di Porto domanda online concorsi.difesa.it InPA"
        ),
        data_pubblicazione="2026-03-23",
        data_apertura="2026-03-23",
        data_scadenza="2026-04-22",
        stimato=0,
        fonte_url="https://concorsi.difesa.it/mm/VFT/2026/Documents/DECRETO_MODIFICA_BANDO_VFT_2026.pdf",
        fonte_tipo="Ministero della Difesa (ufficiale)",
        note="Concorso riservato a militari già in servizio o in congedo (VFI/VFP1), non aperto ai civili.",
    ),
    dict(
        corpo="Esercito Italiano (Forze Speciali)",
        categoria="VFT straordinario - Forze Speciali",
        titolo="Arruolamento straordinario 2026 - 55 posti VFT Forze Speciali (qualifica OBOS)",
        posti="55 posti",
        descrizione=(
            "Concorso straordinario per l'ammissione alla ferma triennale nel Comparto per le "
            "Operazioni Speciali, riservato a VFI in servizio (anche in rafferma annuale), VFI in "
            "congedo per fine ferma e VFP1 in congedo per fine ferma (fino al 31/12/2026)."
        ),
        testo_indicizzato=(
            "Arruolamento straordinario 2026 Forze Speciali Esercito Italiano OBOS operatori base "
            "operazioni speciali VFT 55 posti riservato VFI VFP1 congedo rafferma annuale"
        ),
        data_pubblicazione="2026-06-01",
        data_apertura="2026-06-01",
        data_scadenza="2026-07-23",
        stimato=0,
        fonte_url="https://www.esercito.difesa.it/concorsi-e-arruolamenti/forze-speciali/arruolamento-2026/189121.html",
        fonte_tipo="Esercito Italiano (ufficiale)",
        note="Concorso riservato a militari già in servizio o in congedo, non aperto ai civili.",
    ),
    dict(
        corpo="Marina Militare",
        categoria="VFI (Volontari Ferma Iniziale) - 2° blocco",
        titolo="Concorso VFI Marina Militare 2026 - 2° blocco (550 posti)",
        posti="550 posti (2° blocco; 1.950 nel 1° blocco, già chiuso il 26/11/2025)",
        descrizione=(
            "Reclutamento di Volontari in Ferma Prefissata Iniziale per il Corpo Equipaggi Militari "
            "Marittimi (CEMM) e il Corpo delle Capitanerie di Porto, con incorporamenti scaglionati "
            "da giugno 2026 a gennaio 2027. Aperto anche ai civili in possesso dei requisiti generali."
        ),
        testo_indicizzato=(
            "Concorso VFI Marina Militare 2026 volontari ferma prefissata iniziale CEMM Capitanerie "
            "di Porto Guardia Costiera secondo blocco domanda online concorsi.difesa.it SPID CIE "
            "prove efficienza fisica composizione corporea forza muscolare massa metabolicamente attiva "
            "settori speciali incursori palombari aeromobili soccorritori marittimi Mariscuola Taranto"
        ),
        data_pubblicazione="2025-10-27",
        data_apertura="2026-07-01",
        data_scadenza="2026-07-30",
        stimato=0,
        fonte_url="https://concorsi.difesa.it/mm/VFI/2026/Documents/Bando_VFI_MM_2026.pdf",
        fonte_tipo="Ministero della Difesa (ufficiale)",
        note="Bando aperto anche a candidati civili.",
    ),
    dict(
        corpo="Aeronautica Militare",
        categoria="VFI (Volontari Ferma Iniziale)",
        titolo="Concorso VFI Aeronautica Militare 2026 - 1.050 posti",
        posti="1.050 posti (1.000 ruoli ordinari + 50 COMOS STOS/Incursori)",
        descrizione=(
            "Reclutamento di Volontari in Ferma Prefissata Iniziale nei ruoli ordinari e nel settore "
            "impiego COMOS (STOS/Incursori). Prova culturale prevista dalla seconda settimana di "
            "giugno 2026 presso il Centro di Selezione di Foligno (PG)."
        ),
        testo_indicizzato=(
            "Concorso VFI Aeronautica Militare 2026 volontari ferma prefissata iniziale ruoli "
            "ordinari COMOS STOS incursori prova culturale Centro Selezione Foligno giugno 2026"
        ),
        data_pubblicazione="2025-10-23",
        data_apertura="2025-10-23",
        data_scadenza="2025-11-21",
        stimato=0,
        fonte_url="https://concorsi.difesa.it/am/VFI/2026/Pagine/home.aspx",
        fonte_tipo="Ministero della Difesa (ufficiale)",
        note="Domande chiuse; utile per capire tempistiche/struttura in vista della prossima edizione.",
    ),
    dict(
        corpo="Arma dei Carabinieri",
        categoria="Allievi Carabinieri (ruolo Appuntati e Carabinieri)",
        titolo="Concorso Allievi Carabinieri 2026 - 3.081 posti",
        posti="3.081 posti (2.134 riservati a VFP in servizio/congedo, 915 civili, 32 bilinguismo)",
        descrizione=(
            "Concorso pubblico per il reclutamento di Allievi Carabinieri in ferma quadriennale. "
            "Requisiti generali: età non superiore a 24 anni per i civili, diploma di istruzione "
            "secondaria di secondo grado, idoneità psicofisica al servizio militare incondizionato."
        ),
        testo_indicizzato=(
            "Concorso Allievi Carabinieri 2026 ferma quadriennale ruolo Appuntati Carabinieri civili "
            "VFP riservati bilinguismo Portale Concorsi Online Arma dei Carabinieri diploma idoneita "
            "psicofisica servizio militare incondizionato eta 24 anni"
        ),
        data_pubblicazione="2026-03-07",
        data_apertura="2026-03-07",
        data_scadenza="2026-04-07",
        stimato=0,
        fonte_url="https://www.carabinieri.it/docs/default-source/concorsi/2026/mo208/bando-di-concorso.pdf",
        fonte_tipo="Arma dei Carabinieri (ufficiale)",
        note="Aperto anche a candidati civili.",
    ),
    dict(
        corpo="Arma dei Carabinieri",
        categoria="Allievi Marescialli (ruolo Ispettori)",
        titolo="Concorso 16° Corso Allievi Marescialli Carabinieri 2026-2029 - 898 posti",
        posti="898 posti (199 riservati a categorie specifiche, 36 specializzazione forestale/ambientale/agroalimentare)",
        descrizione=(
            "Concorso per titoli ed esami per l'ammissione al 16° Corso Triennale di Allievi "
            "Marescialli del ruolo Ispettori. Requisiti: età tra 17 e 26 anni alla scadenza della domanda."
        ),
        testo_indicizzato=(
            "Concorso 16 corso allievi marescialli carabinieri 2026 2029 ruolo ispettori 898 posti "
            "Scuola Marescialli e Brigadieri dei Carabinieri SPID CIE eta 17 26 anni"
        ),
        data_pubblicazione="2026-02-18",
        data_apertura="2026-02-18",
        data_scadenza="2026-03-19",
        stimato=0,
        fonte_url="https://www.carabinieri.it/concorsi/area-concorsi/concorsi-pubblici/concorso-per-titoli-ed-esami-per-ammissione-al-16-corso-triennale-2026-2029-di-898-allievi-marescialli-del-ruolo-ispettori-dell-arma-dei-carabinieri",
        fonte_tipo="Arma dei Carabinieri (ufficiale)",
        note="",
    ),
    dict(
        corpo="Guardia di Finanza",
        categoria="Allievi Marescialli",
        titolo="Concorso Allievi Marescialli Guardia di Finanza 2026 - 983 posti",
        posti="983 posti",
        descrizione=(
            "Concorso pubblico per titoli ed esami per l'ammissione di 983 Allievi Marescialli al "
            "98° corso presso la Scuola Ispettori e Sovrintendenti della Guardia di Finanza."
        ),
        testo_indicizzato=(
            "Concorso Allievi Marescialli Guardia di Finanza 2026 983 posti 98 corso Scuola Ispettori "
            "Sovrintendenti diplomati"
        ),
        data_pubblicazione="2026-01-22",
        data_apertura="2026-01-22",
        data_scadenza="2026-03-23",
        stimato=0,
        fonte_url="https://www.gdf.gov.it/concorsi",
        fonte_tipo="Fonte secondaria - verificare su gdf.gov.it",
        note="Dati aggregati da fonti secondarie: verificare testo e date sul portale ufficiale gdf.gov.it.",
    ),
    dict(
        corpo="Guardia di Finanza",
        categoria="Allievi Ufficiali (Accademia)",
        titolo="Concorso Allievi Ufficiali Guardia di Finanza 2026/2027 - 69 posti",
        posti="69 posti",
        descrizione=(
            "Concorso per l'ammissione al corso di Accademia per Allievi Ufficiali, anno accademico "
            "2026/2027. Requisiti: età tra 17 e 22 anni non compiuti al 1° gennaio 2026, diploma di "
            "istruzione secondaria di secondo grado."
        ),
        testo_indicizzato=(
            "Concorso Allievi Ufficiali Guardia di Finanza Accademia 2026 2027 69 posti eta 17 22 anni "
            "diploma pilota elicottero adattabilita"
        ),
        data_pubblicazione="2026-01-15",
        data_apertura="2026-01-15",
        data_scadenza="2026-02-14",
        stimato=0,
        fonte_url="https://www.gdf.gov.it/concorsi",
        fonte_tipo="Fonte secondaria - verificare su gdf.gov.it",
        note="Dati aggregati da fonti secondarie: verificare testo e date sul portale ufficiale gdf.gov.it.",
    ),
    dict(
        corpo="Guardia di Finanza",
        categoria="Allievi Finanzieri",
        titolo="Concorso Allievi Finanzieri 2026 (previsto)",
        posti="Da definire",
        descrizione=(
            "Nuovo bando per la carriera di Finanziere di truppa atteso indicativamente entro ottobre "
            "2026, sulla base della cadenza storica delle uscite precedenti. Data e numero posti non "
            "ancora ufficiali."
        ),
        testo_indicizzato=(
            "Concorso Allievi Finanzieri 2026 previsto stima ottobre truppa Guardia di Finanza"
        ),
        data_pubblicazione=None,
        data_apertura=None,
        data_scadenza=None,
        stimato=1,
        fonte_url="https://www.gdf.gov.it/concorsi",
        fonte_tipo="Stima su base storica - nessun bando pubblicato",
        note="STIMA non ufficiale basata su cadenza storica: nessun bando risulta ancora pubblicato.",
    ),
]

# Domande quiz originali (non tratte da raccolte terze), organizzate per materia.
# Q, opzioni A-D, risposta corretta (lettera), spiegazione.
QUIZ_QUESTIONS = [
    # Educazione civica e Costituzione
    ("Educazione civica", "Chi è il Comandante supremo delle Forze Armate secondo la Costituzione italiana?",
     "Il Presidente del Consiglio", "Il Presidente della Repubblica", "Il Ministro della Difesa", "Il Capo di Stato Maggiore della Difesa",
     "B", "Art. 87 della Costituzione: il Presidente della Repubblica ha il comando delle Forze Armate e presiede il Consiglio Supremo di Difesa."),
    ("Educazione civica", "Quale articolo della Costituzione sancisce che 'La Repubblica ripudia la guerra come strumento di offesa alla libertà degli altri popoli'?",
     "Articolo 3", "Articolo 5", "Articolo 11", "Articolo 21",
     "C", "È l'articolo 11 della Costituzione italiana."),
    ("Educazione civica", "In base alla Costituzione, la difesa della Patria è:",
     "Un dovere solo per i militari di carriera", "Sacro dovere del cittadino", "Facoltativa", "Regolata solo da leggi ordinarie",
     "B", "Art. 52 Cost.: 'La difesa della Patria è sacro dovere del cittadino'."),
    ("Educazione civica", "Quante sono le Camere del Parlamento italiano?",
     "Una", "Due", "Tre", "Quattro",
     "B", "Il Parlamento italiano è bicamerale: Camera dei Deputati e Senato della Repubblica."),
    ("Educazione civica", "Chi nomina il Presidente del Consiglio dei Ministri?",
     "Il Parlamento", "Il Presidente della Repubblica", "La Corte Costituzionale", "Il Consiglio Supremo di Difesa",
     "B", "Art. 92 Cost.: il Presidente della Repubblica nomina il Presidente del Consiglio e, su proposta di questo, i Ministri."),
    ("Educazione civica", "Qual è l'organo che esercita il controllo di costituzionalità delle leggi in Italia?",
     "Il Consiglio di Stato", "La Corte dei Conti", "La Corte Costituzionale", "Il Consiglio Superiore della Magistratura",
     "C", "La Corte Costituzionale giudica sulla legittimità costituzionale delle leggi (art. 134 Cost.)."),
    ("Educazione civica", "A quale età si acquisisce il diritto di voto per la Camera dei Deputati?",
     "16 anni", "18 anni", "21 anni", "25 anni",
     "B", "Dopo la riforma costituzionale del 2021, il diritto di voto per entrambe le Camere si acquisisce a 18 anni."),
    ("Educazione civica", "Il Consiglio Supremo di Difesa è presieduto da:",
     "Il Ministro della Difesa", "Il Presidente della Repubblica", "Il Presidente del Consiglio", "Il Capo di Stato Maggiore della Difesa",
     "B", "Art. 87 Cost.: il Presidente della Repubblica presiede il Consiglio Supremo di Difesa."),
    ("Educazione civica", "Quale principio è espresso dall'articolo 3 della Costituzione?",
     "La libertà di stampa", "L'uguaglianza dei cittadini davanti alla legge", "La libertà religiosa", "Il diritto alla salute",
     "B", "Art. 3 Cost.: principio di uguaglianza formale e sostanziale."),
    ("Educazione civica", "Chi ha il potere di dichiarare lo stato di guerra secondo la Costituzione?",
     "Il Governo autonomamente", "Le Camere, con conferimento dei poteri necessari al Governo", "Il solo Presidente della Repubblica", "Il Consiglio Supremo di Difesa",
     "B", "Art. 78 Cost.: le Camere deliberano lo stato di guerra e conferiscono al Governo i poteri necessari."),

    # Storia
    ("Storia", "In quale anno è terminata la Prima Guerra Mondiale?",
     "1916", "1917", "1918", "1919",
     "C", "La Prima Guerra Mondiale terminò l'11 novembre 1918 con l'armistizio di Compiègne."),
    ("Storia", "Quale battaglia della Prima Guerra Mondiale è considerata la disfatta più grave per l'esercito italiano?",
     "Vittorio Veneto", "Caporetto", "Piave", "Isonzo",
     "B", "La rotta di Caporetto (ottobre-novembre 1917) fu la più grave disfatta italiana della guerra."),
    ("Storia", "In che anno è entrata in vigore la Costituzione della Repubblica Italiana?",
     "1946", "1947", "1948", "1950",
     "C", "La Costituzione, approvata nel dicembre 1947, entrò in vigore il 1° gennaio 1948."),
    ("Storia", "Chi era il Re d'Italia allo scoppio della Prima Guerra Mondiale?",
     "Umberto I", "Vittorio Emanuele II", "Vittorio Emanuele III", "Umberto II",
     "C", "Vittorio Emanuele III regnò dal 1900 al 1946."),
    ("Storia", "In quale anno è nata la Repubblica Italiana, a seguito del referendum istituzionale?",
     "1945", "1946", "1947", "1948",
     "B", "Il referendum del 2 giugno 1946 sancì il passaggio dalla Monarchia alla Repubblica."),
    ("Storia", "Quale evento segna convenzionalmente l'inizio della Seconda Guerra Mondiale?",
     "L'invasione tedesca della Polonia (1939)", "L'attacco a Pearl Harbor (1941)", "L'armistizio dell'8 settembre 1943", "La caduta di Berlino (1945)",
     "A", "L'invasione della Polonia da parte della Germania nel settembre 1939 è considerata l'inizio convenzionale del conflitto in Europa."),
    ("Storia", "Cosa avvenne l'8 settembre 1943 per l'Italia?",
     "La dichiarazione di guerra alla Germania", "L'armistizio con gli Alleati", "La liberazione di Roma", "La fondazione della Repubblica Sociale Italiana",
     "B", "L'8 settembre 1943 fu reso noto l'armistizio di Cassibile tra Italia e Alleati."),
    ("Storia", "Chi fu il primo Presidente della Repubblica Italiana?",
     "Luigi Einaudi", "Enrico De Nicola", "Alcide De Gasperi", "Sandro Pertini",
     "B", "Enrico De Nicola fu il primo Presidente della Repubblica (1948), dopo essere stato Capo provvisorio dello Stato dal 1946."),
    ("Storia", "L'Unità d'Italia fu proclamata nel:",
     "1848", "1861", "1870", "1918",
     "B", "Il Regno d'Italia fu proclamato il 17 marzo 1861."),
    ("Storia", "Quale città fu l'ultima ad essere annessa al Regno d'Italia, nel 1870?",
     "Venezia", "Trento", "Roma", "Trieste",
     "C", "Roma fu annessa nel 1870 dopo la breccia di Porta Pia."),

    # Geografia
    ("Geografia", "Qual è il fiume più lungo d'Italia?",
     "Tevere", "Po", "Adige", "Arno",
     "B", "Il Po, con circa 652 km, è il fiume più lungo d'Italia."),
    ("Geografia", "Quante sono le Regioni italiane?",
     "18", "19", "20", "21",
     "C", "L'Italia è divisa in 20 Regioni, di cui 5 a statuto speciale."),
    ("Geografia", "Qual è la vetta più alta delle Alpi italiane?",
     "Monte Bianco", "Cervino", "Gran Paradiso", "Monte Rosa",
     "A", "Il Monte Bianco (4.809 m) è la vetta più alta delle Alpi, condivisa con la Francia."),
    ("Geografia", "Quale mare bagna la costa orientale dell'Italia?",
     "Mar Ligure", "Mar Tirreno", "Mar Adriatico", "Mar Ionio",
     "C", "Il Mar Adriatico bagna il versante orientale della penisola italiana."),
    ("Geografia", "Qual è la regione italiana con la superficie più estesa?",
     "Piemonte", "Sicilia", "Lombardia", "Toscana",
     "B", "La Sicilia è la regione più estesa d'Italia (circa 25.700 km²)."),
    ("Geografia", "Su quali isole maggiori si estendono rispettivamente la Sicilia e la Sardegna?",
     "Sono la stessa isola", "Sono le due isole maggiori italiane nel Mediterraneo", "Sono arcipelaghi minori", "Appartengono ad altri stati",
     "B", "Sicilia e Sardegna sono le due isole maggiori italiane."),
    ("Geografia", "Qual è la capitale della Regione Veneto?",
     "Verona", "Padova", "Venezia", "Vicenza",
     "C", "Venezia è il capoluogo di regione del Veneto."),
    ("Geografia", "Quale catena montuosa attraversa l'Italia da nord a sud?",
     "Le Alpi", "Gli Appennini", "I Pirenei", "I Carpazi",
     "B", "Gli Appennini attraversano longitudinalmente l'intera penisola italiana."),
    ("Geografia", "Con quanti Stati confina l'Italia via terra?",
     "3", "4", "5", "6",
     "C", "L'Italia confina con Francia, Svizzera, Austria, Slovenia e la Città del Vaticano/San Marino (enclave); considerando i confini terrestri principali con stati esteri: Francia, Svizzera, Austria, Slovenia (4 stati esteri) più le due enclavi di San Marino e Vaticano: la risposta comunemente accettata nei quiz è 5 includendo le enclavi."),
    ("Geografia", "Qual è il vulcano attivo più alto d'Europa?",
     "Vesuvio", "Stromboli", "Etna", "Vulcano",
     "C", "L'Etna, in Sicilia, con oltre 3.300 m, è il vulcano attivo più alto d'Europa."),

    # Logica e matematica di base
    ("Logica e matematica", "Se un percorso di 12 km viene coperto in 1 ora e 30 minuti, qual è la velocità media?",
     "6 km/h", "8 km/h", "9 km/h", "12 km/h",
     "B", "12 km / 1,5 h = 8 km/h."),
    ("Logica e matematica", "Completa la serie: 2, 4, 8, 16, ...",
     "20", "24", "32", "30",
     "C", "La serie raddoppia ogni termine: 16 × 2 = 32."),
    ("Logica e matematica", "Quale numero è il successivo nella serie 3, 6, 9, 12, ...?",
     "13", "14", "15", "16",
     "C", "La serie procede di 3 in 3: 12 + 3 = 15."),
    ("Logica e matematica", "Se 5 operai completano un lavoro in 8 giorni, in quanti giorni lo completano 10 operai (a parità di produttività)?",
     "4", "8", "16", "2",
     "A", "Raddoppiando gli operai il tempo si dimezza: 8/2 = 4 giorni."),
    ("Logica e matematica", "Qual è il 25% di 200?",
     "25", "50", "75", "100",
     "B", "200 × 0,25 = 50."),
    ("Logica e matematica", "'Tutti i militari indossano l'uniforme in servizio. Marco è in servizio.' Cosa si può concludere logicamente?",
     "Marco è un ufficiale", "Marco indossa l'uniforme", "Marco non è un militare", "Non si può concludere nulla",
     "B", "Sillogismo semplice: dalla premessa generale e dal caso particolare segue che Marco indossa l'uniforme."),
    ("Logica e matematica", "Quale numero completa la serie: 1, 1, 2, 3, 5, 8, ...?",
     "10", "11", "13", "12",
     "C", "È la sequenza di Fibonacci: 5 + 8 = 13."),
    ("Logica e matematica", "Un treno viaggia a 90 km/h. Quanti km percorre in 20 minuti?",
     "20 km", "30 km", "45 km", "60 km",
     "B", "20 minuti = 1/3 di ora; 90 × 1/3 = 30 km."),
    ("Logica e matematica", "Se A è maggiore di B e B è maggiore di C, quale relazione è corretta?",
     "A è minore di C", "A è uguale a C", "A è maggiore di C", "Non è determinabile",
     "C", "Per proprietà transitiva, se A > B e B > C allora A > C."),
    ("Logica e matematica", "Quanti sono i multipli di 4 compresi tra 1 e 20 (inclusi)?",
     "3", "4", "5", "6",
     "C", "I multipli di 4 tra 1 e 20 sono 4, 8, 12, 16, 20: cinque numeri."),

    # Ordinamento delle Forze Armate
    ("Ordinamento Forze Armate", "Da chi dipende funzionalmente il Capo di Stato Maggiore della Difesa?",
     "Dal Presidente della Repubblica direttamente", "Dal Ministro della Difesa", "Dal Presidente del Consiglio", "Dal Parlamento",
     "B", "Il Capo di Stato Maggiore della Difesa (CSMD) è il vertice militare che risponde al Ministro della Difesa."),
    ("Ordinamento Forze Armate", "Quali sono le quattro Forze Armate italiane?",
     "Esercito, Marina, Aeronautica, Arma dei Carabinieri", "Esercito, Marina, Guardia di Finanza, Polizia", "Esercito, Aeronautica, Vigili del Fuoco, Marina", "Marina, Aeronautica, Carabinieri, Polizia Penitenziaria",
     "A", "Le Forze Armate italiane sono Esercito, Marina Militare, Aeronautica Militare e Arma dei Carabinieri (dal 2000 quarta Forza Armata)."),
    ("Ordinamento Forze Armate", "In quale anno l'Arma dei Carabinieri è diventata la quarta Forza Armata a pari dignità con le altre?",
     "1990", "2000", "2005", "2010",
     "B", "Con il D.Lgs. 297/2000 l'Arma dei Carabinieri è stata elevata al rango di quarta Forza Armata."),
    ("Ordinamento Forze Armate", "Cosa significa l'acronimo VFP1?",
     "Volontario in Ferma Prefissata di 1 anno", "Vice Formatore Professionale 1", "Volontario Forze Permanenti 1", "Verifica Fisica Preliminare 1",
     "A", "VFP1 indicava i Volontari in Ferma Prefissata di 1 anno (oggi in gran parte confluiti nella dizione VFI)."),
    ("Ordinamento Forze Armate", "La Guardia di Finanza dipende funzionalmente da quale ministero per i compiti di polizia economico-finanziaria?",
     "Ministero della Difesa", "Ministero dell'Economia e delle Finanze", "Ministero dell'Interno", "Presidenza del Consiglio",
     "B", "La Guardia di Finanza è un corpo militare che dipende dal Ministero dell'Economia e delle Finanze, pur avendo ordinamento militare."),
    ("Ordinamento Forze Armate", "Cosa si intende con VFI?",
     "Volontario in Ferma Iniziale", "Vice Funzionario Ispettivo", "Verifica Finale Idoneità", "Volontario Forze Interforze",
     "A", "VFI sta per Volontario in Ferma Prefissata Iniziale, la nuova denominazione che ha sostituito in gran parte VFP1."),
]

CHECKLIST_TEMPLATE = [
    "Documento d'identità in corso di validità",
    "Codice fiscale / tessera sanitaria",
    "Titolo di studio richiesto dal bando (diploma/attestato)",
    "Ricevuta della domanda presentata sul portale ufficiale (concorsi.difesa.it / carabinieri.it / InPA)",
    "Autocertificazione dei requisiti generali (se richiesta dal bando)",
    "Eventuali titoli preferenziali o di servizio (attestati, congedi, brevetti)",
    "Conferma appuntamento per accertamenti psicofisici/visita medica",
    "Abbigliamento e attrezzatura per le prove di efficienza fisica (secondo indicazioni del bando)",
    "Stampa o salvataggio offline del testo integrale del bando ufficiale di riferimento",
    "Verifica scadenze e documenti da presentare il giorno delle prove (da bando specifico)",
]


def seed_if_empty():
    db = get_db()
    if db.execute("SELECT COUNT(*) FROM bandi").fetchone()[0] == 0:
        for b in BANDI:
            db.execute(
                """INSERT INTO bandi
                (corpo, categoria, titolo, posti, descrizione, testo_indicizzato,
                 data_pubblicazione, data_apertura, data_scadenza, stimato, fonte_url, fonte_tipo, note)
                VALUES (:corpo, :categoria, :titolo, :posti, :descrizione, :testo_indicizzato,
                 :data_pubblicazione, :data_apertura, :data_scadenza, :stimato, :fonte_url, :fonte_tipo, :note)""",
                b,
            )
    if db.execute("SELECT COUNT(*) FROM quiz_questions").fetchone()[0] == 0:
        for q in QUIZ_QUESTIONS:
            db.execute(
                """INSERT INTO quiz_questions
                (materia, domanda, opzione_a, opzione_b, opzione_c, opzione_d, risposta, spiegazione)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                q,
            )
    if db.execute("SELECT COUNT(*) FROM checklist_template").fetchone()[0] == 0:
        for i, testo in enumerate(CHECKLIST_TEMPLATE):
            db.execute(
                "INSERT INTO checklist_template (testo, ordine) VALUES (?, ?)", (testo, i)
            )
    db.commit()
