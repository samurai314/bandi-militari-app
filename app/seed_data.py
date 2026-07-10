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
        posti="Da definire (edizioni recenti: 1.410 nel 2022, 1.673 nel 2023, 1.634 nel 2024, 1.985 nel 2025)",
        descrizione=(
            "Nuovo bando per la carriera di Finanziere di truppa. Le ultime quattro edizioni sono uscite "
            "con cadenza annuale: dicembre 2022, settembre 2023, novembre 2024, ottobre 2025. Su questa "
            "base la finestra più probabile per la prossima edizione è ottobre-novembre 2026, con margine "
            "fino a dicembre 2026. Data e numero posti non ancora ufficiali."
        ),
        testo_indicizzato=(
            "Concorso Allievi Finanzieri 2026 previsto stima ottobre novembre dicembre truppa Guardia di "
            "Finanza cadenza annuale storica 2022 2023 2024 2025"
        ),
        data_pubblicazione=None,
        data_apertura=None,
        data_scadenza=None,
        stimato=1,
        stima_periodo_da="2026-10-01",
        stima_periodo_a="2026-12-31",
        fonte_url="https://www.gdf.gov.it/concorsi",
        fonte_tipo="Stima su base storica - nessun bando pubblicato",
        note=(
            "STIMA non ufficiale basata sulla cadenza delle 4 edizioni precedenti (2022-2025): "
            "nessun bando risulta ancora pubblicato per il 2026."
        ),
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
    ("Ordinamento Forze Armate", "Cosa si intende per 'stato di ferma'?",
     "Un permesso di malattia", "Il periodo di impegno continuativo in servizio militare assunto dal volontario", "Un grado militare", "Una sanzione disciplinare",
     "B", "Lo stato di ferma indica il periodo per cui un volontario si impegna a prestare servizio militare continuativo."),
    ("Ordinamento Forze Armate", "Quale legge ha sospeso la leva obbligatoria in Italia, rendendo le Forze Armate professionali?",
     "Legge 226/2004", "Legge 121/1981", "Legge 382/1978", "Legge 380/1999",
     "A", "La Legge 226/2004 ha sospeso il servizio di leva obbligatorio a partire dal 2005."),
    ("Ordinamento Forze Armate", "Cos'è il Foglio Matricolare di un militare?",
     "Il libretto di circolazione di un mezzo militare", "Il documento che riporta la storia di servizio del militare", "Un buono pasto", "Un permesso di guida",
     "B", "Il Foglio Matricolare riporta la storia di servizio, i gradi e gli eventi di carriera di un militare."),
    ("Ordinamento Forze Armate", "Quale organo consultivo assiste il Presidente della Repubblica in materia di difesa?",
     "Il Consiglio dei Ministri", "Il Consiglio Supremo di Difesa", "Il Consiglio di Stato", "La Corte dei Conti",
     "B", "Il Consiglio Supremo di Difesa, presieduto dal Presidente della Repubblica, ha funzioni consultive in materia di difesa e sicurezza."),
    ("Ordinamento Forze Armate", "Cosa significa 'congedo illimitato' per un militare?",
     "L'espulsione disciplinare", "La cessazione del servizio attivo con permanenza nella riserva", "Una promozione automatica", "Un periodo di ferie prolungate",
     "B", "Il congedo illimitato indica la cessazione dal servizio attivo, con il militare che resta comunque nella riserva."),
    ("Ordinamento Forze Armate", "In quale anno è stato istituito in Italia il servizio militare femminile volontario?",
     "1989", "1999", "2005", "2010",
     "B", "Il servizio militare volontario femminile è stato istituito con la Legge 380/1999."),
    ("Ordinamento Forze Armate", "Quale corpo si occupa della sicurezza e vigilanza degli istituti penitenziari (e non è una Forza Armata)?",
     "L'Arma dei Carabinieri", "La Polizia Penitenziaria", "La Guardia di Finanza", "La Marina Militare",
     "B", "La Polizia Penitenziaria è un corpo di polizia a ordinamento civile, distinto dalle quattro Forze Armate."),

    ("Educazione civica", "Quanti anni dura il mandato del Presidente della Repubblica italiana?",
     "5 anni", "6 anni", "7 anni", "9 anni",
     "C", "Il mandato presidenziale dura 7 anni (art. 85 Cost.)."),
    ("Educazione civica", "Quali sono le Regioni italiane a statuto speciale?",
     "Solo Sicilia e Sardegna", "Valle d'Aosta, Trentino-Alto Adige, Friuli-Venezia Giulia, Sicilia, Sardegna", "Tutte le regioni del Nord", "Nessuna, sono state abolite",
     "B", "Le cinque Regioni a statuto speciale sono Valle d'Aosta, Trentino-Alto Adige, Friuli-Venezia Giulia, Sicilia e Sardegna."),
    ("Educazione civica", "Cos'è un referendum abrogativo?",
     "Uno strumento per eleggere il Parlamento", "Uno strumento con cui i cittadini possono abrogare in tutto o in parte una legge", "Una legge costituzionale", "Un tipo di decreto legge",
     "B", "L'art. 75 Cost. prevede il referendum popolare per deliberare l'abrogazione totale o parziale di una legge."),
    ("Educazione civica", "Qual è la differenza principale tra decreto legge e decreto legislativo?",
     "Sono sinonimi", "Il decreto legge è adottato dal Governo per necessità e urgenza e va convertito entro 60 giorni, il decreto legislativo è emanato su delega del Parlamento", "Il decreto legislativo lo emana solo il Presidente della Repubblica", "Il decreto legge non ha mai valore di legge",
     "B", "Il decreto legge (art. 77 Cost.) richiede conversione in legge entro 60 giorni; il decreto legislativo (art. 76 Cost.) è emanato su delega del Parlamento tramite legge delega."),
    ("Educazione civica", "Cosa tutela l'articolo 21 della Costituzione italiana?",
     "Il diritto alla salute", "La libertà di manifestazione del pensiero", "Il diritto di proprietà", "La libertà di circolazione",
     "B", "L'articolo 21 tutela la libertà di manifestare il proprio pensiero con la parola, lo scritto e ogni altro mezzo di diffusione."),
    ("Educazione civica", "Quale organo esercita il controllo sulla gestione del bilancio e della finanza pubblica in Italia?",
     "La Corte dei Conti", "La Corte Costituzionale", "Il Consiglio di Stato", "La Banca d'Italia",
     "A", "La Corte dei Conti esercita il controllo sulla gestione finanziaria degli enti pubblici e sul bilancio dello Stato."),
    ("Educazione civica", "Cosa prevede in sintesi l'immunità parlamentare (art. 68 Cost.)?",
     "I parlamentari non pagano le tasse", "I parlamentari non possono essere perseguiti per le opinioni espresse nell'esercizio delle loro funzioni", "I parlamentari sono esenti dal servizio militare", "I parlamentari non possono essere licenziati",
     "B", "L'art. 68 Cost. tutela i parlamentari da azioni giudiziarie per le opinioni espresse e i voti dati nell'esercizio delle funzioni."),
    ("Educazione civica", "Cosa si intende per principio di sussidiarietà nell'ordinamento italiano?",
     "Che lo Stato decide sempre su tutto", "Che le decisioni pubbliche vanno prese al livello di governo più vicino ai cittadini, quando possibile", "Che le Regioni non hanno alcun potere", "Che i Comuni dipendono sempre dalle Regioni",
     "B", "Il principio di sussidiarietà favorisce l'esercizio delle funzioni pubbliche al livello di governo più vicino ai cittadini, quando adeguato."),
    ("Educazione civica", "A quale età si può oggi essere eletti alla Camera dei Deputati?",
     "18 anni", "21 anni", "25 anni", "40 anni",
     "A", "Dopo la riforma costituzionale del 2021, l'età per essere eletti alla Camera è stata uniformata a 18 anni, come per il Senato."),

    ("Storia", "In che anno cadde il Muro di Berlino?",
     "1985", "1987", "1989", "1991",
     "C", "Il Muro di Berlino cadde il 9 novembre 1989."),
    ("Storia", "In quale anno Mussolini prese il potere con la Marcia su Roma?",
     "1918", "1922", "1925", "1929",
     "B", "La Marcia su Roma avvenne nell'ottobre 1922, portando Mussolini alla guida del Governo."),
    ("Storia", "In quale anno fu firmata la Dichiarazione Universale dei Diritti dell'Uomo?",
     "1945", "1948", "1950", "1955",
     "B", "La Dichiarazione Universale dei Diritti dell'Uomo fu adottata dall'ONU nel 1948."),
    ("Storia", "In quale anno l'Italia entrò a far parte della Comunità Economica Europea (Trattati di Roma)?",
     "1950", "1957", "1965", "1970",
     "B", "I Trattati di Roma, che istituirono la CEE, furono firmati nel 1957."),
    ("Storia", "Quale trattato ha istituito l'Unione Europea nella sua forma attuale?",
     "Trattato di Roma", "Trattato di Maastricht", "Trattato di Lisbona", "Trattato di Amsterdam",
     "B", "Il Trattato di Maastricht (1992) istituì formalmente l'Unione Europea."),
    ("Storia", "Cosa avvenne il 25 luglio 1943 in Italia?",
     "La liberazione di Roma", "La sfiducia del Gran Consiglio del Fascismo a Mussolini e il suo conseguente arresto", "L'armistizio con gli Alleati", "L'inizio della Resistenza",
     "B", "Il 25 luglio 1943 il Gran Consiglio del Fascismo sfiduciò Mussolini, che fu arrestato subito dopo su ordine del Re."),
    ("Storia", "Cos'è stata la Resistenza italiana?",
     "Un partito politico del dopoguerra", "Il movimento di lotta partigiana contro il nazifascismo tra il 1943 e il 1945", "Un'operazione militare alleata in Sicilia", "Un trattato di pace",
     "B", "La Resistenza fu il movimento di lotta armata e civile contro l'occupazione nazifascista tra il 1943 e il 1945."),
    ("Storia", "In quale data si celebra la Festa della Liberazione in Italia?",
     "2 giugno", "4 novembre", "25 aprile", "20 settembre",
     "C", "Il 25 aprile si celebra la Liberazione dal nazifascismo (25 aprile 1945)."),
    ("Storia", "In quale anno è avvenuta la riunificazione della Germania dopo la Guerra Fredda?",
     "1985", "1990", "1995", "2000",
     "B", "La riunificazione tedesca avvenne ufficialmente nel 1990, dopo la caduta del Muro di Berlino nel 1989."),

    ("Geografia", "Qual è la regione italiana più piccola per superficie?",
     "Molise", "Valle d'Aosta", "Liguria", "Umbria",
     "B", "La Valle d'Aosta è la regione italiana più piccola per superficie."),
    ("Geografia", "Qual è il lago più grande d'Italia?",
     "Lago di Como", "Lago di Garda", "Lago Maggiore", "Lago Trasimeno",
     "B", "Il Lago di Garda è il lago più esteso d'Italia."),
    ("Geografia", "Qual è il capoluogo della Regione Sicilia?",
     "Catania", "Messina", "Palermo", "Siracusa",
     "C", "Palermo è il capoluogo della Regione Siciliana."),
    ("Geografia", "Quale stretto separa la Sicilia dalla Calabria?",
     "Stretto di Bonifacio", "Stretto di Messina", "Stretto di Otranto", "Stretto dei Dardanelli",
     "B", "Lo Stretto di Messina separa la Sicilia dalla Calabria, sulla terraferma italiana."),
    ("Geografia", "Qual è l'isola italiana situata più a sud, nel Canale di Sicilia?",
     "Pantelleria", "Lampedusa", "Favignana", "Ustica",
     "B", "Lampedusa, nel Canale di Sicilia, è l'isola italiana più meridionale."),
    ("Geografia", "Quante delle 20 regioni italiane si affacciano sul mare?",
     "10", "12", "15", "18",
     "C", "15 regioni italiane sono costiere; le rimanenti 5 (Valle d'Aosta, Piemonte, Lombardia, Trentino-Alto Adige, Umbria) non hanno sbocco sul mare."),
    ("Geografia", "Quale fiume attraversa la città di Roma?",
     "Arno", "Tevere", "Po", "Adige",
     "B", "Il Tevere attraversa la città di Roma."),
    ("Geografia", "Qual è la vetta più alta della catena degli Appennini?",
     "Monte Amiata", "Corno Grande (Gran Sasso)", "Monte Vettore", "Monte Terminillo",
     "B", "Il Corno Grande, nel massiccio del Gran Sasso, con 2.912 m è la vetta più alta degli Appennini."),
    ("Geografia", "Quali due mari si incontrano nello Stretto di Messina?",
     "Adriatico e Ionio", "Tirreno e Ionio", "Ligure e Tirreno", "Adriatico e Tirreno",
     "B", "Nello Stretto di Messina si incontrano il Mar Tirreno e il Mar Ionio."),
    ("Geografia", "Qual è la seconda città più popolosa d'Italia?",
     "Napoli", "Torino", "Milano", "Palermo",
     "C", "Milano è la seconda città italiana per popolazione dopo Roma."),

    ("Logica e matematica", "Un oggetto costa 80€ e viene scontato del 25%. Quanto costa dopo lo sconto?",
     "50€", "55€", "60€", "65€",
     "C", "Lo sconto del 25% su 80€ è 20€; 80 - 20 = 60€."),
    ("Logica e matematica", "Completa la serie: 5, 10, 20, 40, ...",
     "60", "70", "80", "90",
     "C", "La serie raddoppia ogni termine: 40 × 2 = 80."),
    ("Logica e matematica", "Se 3 penne costano 6€, quanto costano 7 penne (stesso prezzo unitario)?",
     "12€", "14€", "16€", "18€",
     "B", "Ogni penna costa 2€; 7 penne costano 14€."),
    ("Logica e matematica", "Quanto è il 15% di 300?",
     "30", "35", "45", "50",
     "C", "300 × 0,15 = 45."),
    ("Logica e matematica", "Un'auto percorre 240 km in 3 ore. Qual è la sua velocità media?",
     "60 km/h", "70 km/h", "80 km/h", "90 km/h",
     "C", "240 km / 3 h = 80 km/h."),
    ("Logica e matematica", "Completa la serie decrescente: 100, 90, 80, 70, ...",
     "50", "55", "60", "65",
     "C", "La serie decresce di 10 in 10: 70 - 10 = 60."),
    ("Logica e matematica", "'Nessun pesce vola. Il tonno è un pesce.' Cosa si può concludere logicamente?",
     "Il tonno vola", "Il tonno non vola", "Il tonno non è un pesce", "Non si può concludere nulla",
     "B", "Sillogismo: dalla premessa generale segue che il tonno, essendo un pesce, non vola."),
    ("Logica e matematica", "Quanti minuti sono 2 ore e mezza?",
     "120", "130", "150", "180",
     "C", "2 ore e mezza equivalgono a 150 minuti (2×60 + 30)."),
    ("Logica e matematica", "Un magazzino ha 120 scatole e ne vengono vendute il 40%. Quante scatole restano?",
     "48", "60", "72", "80",
     "C", "Il 40% di 120 è 48 (vendute); restano 120 - 48 = 72 scatole."),
    ("Logica e matematica", "Se A=2, B=4, C=8 seguendo un raddoppio progressivo, quale numero completa la sequenza con D?",
     "10", "12", "16", "20",
     "C", "La sequenza raddoppia ogni termine: 8 × 2 = 16."),
]

# Domande ad-hoc allineate alle materie tipicamente richieste per specifici corpi
# (nessuna banca dati ufficiale di domande esiste per questi concorsi — verificato —
# quindi materiale originale, ma sulle materie realmente attinenti al ruolo).
# Formato: (corpo_specifico, materia, domanda, A, B, C, D, risposta, spiegazione)
QUIZ_QUESTIONS_CORPO = [
    ("Carabinieri", "Diritto e ordinamento giudiziario",
     "Quale ruolo ha l'Arma dei Carabinieri rispetto all'autorità giudiziaria?",
     "Nessuno, opera solo su base militare", "Agisce anche come polizia giudiziaria su delega della magistratura",
     "Sostituisce il magistrato nelle indagini", "Ha potere di condanna autonomo",
     "B", "L'Arma svolge anche funzioni di polizia giudiziaria, conducendo indagini sotto la direzione del Pubblico Ministero."),
    ("Carabinieri", "Diritto e ordinamento giudiziario",
     "Chi dirige le indagini preliminari in un procedimento penale italiano?",
     "Il Giudice", "Il Pubblico Ministero", "Il Prefetto", "Il Ministro della Giustizia",
     "B", "Le indagini preliminari sono dirette dal Pubblico Ministero, che si avvale della polizia giudiziaria."),
    ("Carabinieri", "Diritto e ordinamento giudiziario",
     "Qual è la differenza principale tra reato e illecito amministrativo?",
     "Nessuna, sono sinonimi", "Il reato prevede sanzioni penali, l'illecito amministrativo sanzioni pecuniarie amministrative",
     "L'illecito amministrativo è sempre più grave", "Solo i reati sono scritti in una legge",
     "B", "Il reato è punito con sanzioni penali (es. reclusione o multa), l'illecito amministrativo con sanzioni pecuniarie amministrative."),
    ("Carabinieri", "Diritto e ordinamento giudiziario",
     "Chi convalida un arresto in flagranza di reato, ed entro quanto tempo?",
     "Il GIP, entro 96 ore", "Il Sindaco, entro 24 ore", "Il Prefetto, entro 12 ore", "Non serve convalida",
     "A", "L'arresto in flagranza deve essere convalidato dal Giudice per le indagini preliminari entro 96 ore."),
    ("Carabinieri", "Diritto e ordinamento giudiziario",
     "Quale articolo della Costituzione tutela la libertà personale?",
     "Articolo 3", "Articolo 13", "Articolo 21", "Articolo 41",
     "B", "L'articolo 13 della Costituzione tutela l'inviolabilità della libertà personale."),
    ("Carabinieri", "Diritto e ordinamento giudiziario",
     "Cosa si intende per 'fermo di polizia giudiziaria'?",
     "Una multa amministrativa", "Una misura precautelare che priva della libertà un indiziato grave in caso di urgenza",
     "Un controllo documenti di routine", "Una sanzione disciplinare militare",
     "B", "Il fermo è una misura precautelare adottabile in casi di urgenza su soggetti gravemente indiziati di un reato."),
    ("Carabinieri", "Diritto e ordinamento giudiziario",
     "Come è organizzata territorialmente l'Arma dei Carabinieri, a partire dall'unità più piccola?",
     "Stazione, Compagnia, Comando Provinciale", "Solo Comandi Regionali", "Non ha un'articolazione territoriale",
     "Squadra, Battaglione, Divisione",
     "A", "L'organizzazione territoriale parte dalla Stazione, sale a Compagnia e poi a Comando Provinciale."),
    ("Carabinieri", "Diritto e ordinamento giudiziario",
     "Chi ha la titolarità dell'azione penale in Italia?",
     "La polizia", "Il Pubblico Ministero", "La vittima del reato", "Il Parlamento",
     "B", "L'art. 112 Cost. sancisce l'obbligatorietà dell'azione penale in capo al Pubblico Ministero."),

    ("Guardia di Finanza", "Economia e finanza pubblica",
     "Qual è il compito istituzionale principale della Guardia di Finanza?",
     "Solo la difesa dei confini terrestri", "Prevenzione e repressione delle violazioni economico-finanziarie e tributarie",
     "La gestione delle carceri", "La regolazione del traffico urbano",
     "B", "La Guardia di Finanza è il corpo di polizia economico-finanziaria dello Stato italiano."),
    ("Guardia di Finanza", "Economia e finanza pubblica",
     "Cosa si intende per evasione fiscale?",
     "Il pagamento anticipato delle tasse", "La sottrazione illecita di base imponibile o imposta dovuta",
     "Un incentivo fiscale legale", "Una tassa comunale",
     "B", "L'evasione fiscale consiste nel sottrarre illecitamente base imponibile o imposta dovuta al fisco."),
    ("Guardia di Finanza", "Economia e finanza pubblica",
     "Cos'è l'IVA?",
     "Un'imposta sul reddito delle persone fisiche", "Un'imposta indiretta sul valore aggiunto nei consumi",
     "Un contributo previdenziale", "Una tassa di successione",
     "B", "L'IVA (Imposta sul Valore Aggiunto) è un'imposta indiretta che grava sui consumi."),
    ("Guardia di Finanza", "Economia e finanza pubblica",
     "Qual è l'ente principale responsabile della riscossione dei tributi in Italia?",
     "L'INPS", "L'Agenzia delle Entrate", "La Banca d'Italia", "La Corte dei Conti",
     "B", "L'Agenzia delle Entrate gestisce l'accertamento e la riscossione dei tributi, con Agenzia Entrate-Riscossione per la riscossione coattiva."),
    ("Guardia di Finanza", "Economia e finanza pubblica",
     "Cosa distingue l'elusione fiscale dall'evasione fiscale?",
     "Sono la stessa cosa", "L'elusione aggira abusivamente lo scopo della norma senza violarla direttamente, l'evasione la viola apertamente",
     "L'elusione è sempre penalmente rilevante, l'evasione mai", "L'elusione riguarda solo le imprese estere",
     "B", "L'elusione sfrutta abusivamente le norme senza violarle letteralmente; l'evasione le viola direttamente."),
    ("Guardia di Finanza", "Economia e finanza pubblica",
     "La Guardia di Finanza opera anche in mare?",
     "No, solo su base terrestre", "Sì, con reparti navali e aerei per il contrasto ai traffici illeciti",
     "Solo nei porti turistici", "Solo in acque internazionali",
     "B", "La Guardia di Finanza dispone di reparti navali e aerei per il contrasto ai traffici illeciti via mare."),
    ("Guardia di Finanza", "Economia e finanza pubblica",
     "Da quale ministero riceve la Guardia di Finanza l'indirizzo funzionale per i compiti economico-finanziari?",
     "Ministero della Difesa", "Ministero dell'Economia e delle Finanze", "Ministero della Giustizia", "Ministero degli Affari Esteri",
     "B", "Per i compiti di polizia economico-finanziaria la GdF dipende funzionalmente dal Ministero dell'Economia e delle Finanze."),
    ("Guardia di Finanza", "Economia e finanza pubblica",
     "Cosa indica il termine 'base imponibile'?",
     "L'aliquota applicata a un'imposta", "L'importo su cui si applica l'aliquota per calcolare l'imposta dovuta",
     "Il totale delle tasse comunali", "Il reddito minimo esente da tasse",
     "B", "La base imponibile è l'importo a cui si applica l'aliquota fiscale per determinare l'imposta dovuta."),

    ("Esercito/Marina/Aeronautica", "Gradi e ordinamento militare",
     "Qual è, in linea generale, il grado più alto nella gerarchia dell'Esercito Italiano in tempo di pace?",
     "Colonnello", "Generale", "Maresciallo Maggiore", "Capitano",
     "B", "Il grado di Generale (nelle sue varie articolazioni) è il vertice della gerarchia degli ufficiali dell'Esercito."),
    ("Esercito/Marina/Aeronautica", "Gradi e ordinamento militare",
     "Come si chiama nella Marina Militare il grado equivalente a 'Generale'?",
     "Comandante", "Ammiraglio", "Capitano di Vascello", "Nostromo",
     "B", "Nella Marina Militare il grado apicale corrispondente è quello di Ammiraglio."),
    ("Esercito/Marina/Aeronautica", "Gradi e ordinamento militare",
     "Cosa distingue in generale un sottufficiale da un ufficiale?",
     "Nessuna differenza sostanziale", "Il sottufficiale ha funzioni tecniche e di comando intermedio, l'ufficiale funzioni di comando di più alto livello",
     "Il sottufficiale comanda sempre l'intero reparto", "Solo gli ufficiali indossano l'uniforme",
     "B", "I sottufficiali (es. sergenti, marescialli) svolgono funzioni tecniche e di comando intermedio; gli ufficiali (da sottotenente in su) hanno responsabilità di comando più ampie."),
    ("Esercito/Marina/Aeronautica", "Gradi e ordinamento militare",
     "Cos'è il CEMM nella Marina Militare?",
     "Un tipo di nave da guerra", "Il Corpo Equipaggi Militari Marittimi, personale non ufficiale della Marina",
     "Un'accademia navale", "Un grado di ufficiale superiore",
     "B", "Il CEMM (Corpo Equipaggi Militari Marittimi) comprende il personale non ufficiale della Marina Militare."),
    ("Esercito/Marina/Aeronautica", "Gradi e ordinamento militare",
     "Quale grado ricopre tipicamente chi comanda una compagnia nell'Esercito Italiano?",
     "Capitano", "Generale", "Caporal Maggiore", "Ammiraglio",
     "A", "Il comando di una compagnia è tipicamente affidato a un ufficiale con il grado di Capitano."),
    ("Esercito/Marina/Aeronautica", "Gradi e ordinamento militare",
     "Qual è la denominazione del primo grado di un Volontario in Ferma Iniziale (a seconda della Forza Armata)?",
     "Soldato, Marinaio o Aviere", "Generale", "Maresciallo", "Sottotenente",
     "A", "Il grado iniziale di un VFI è Soldato (Esercito), Marinaio (Marina) o Aviere (Aeronautica), a seconda della Forza Armata."),
    ("Esercito/Marina/Aeronautica", "Gradi e ordinamento militare",
     "Chi è il vertice di comando di ciascuna singola Forza Armata (Esercito, Marina, Aeronautica)?",
     "Il Ministro della Difesa", "Il Capo di Stato Maggiore della singola Forza Armata", "Il Presidente della Repubblica direttamente", "Il Capo del Governo",
     "B", "Ogni Forza Armata ha un proprio Capo di Stato Maggiore, vertice tecnico-operativo della Forza Armata stessa."),
    ("Esercito/Marina/Aeronautica", "Gradi e ordinamento militare",
     "Qual è la durata tipica della prima ferma di un Volontario in Ferma Iniziale (VFI)?",
     "Un anno, con possibilità di rafferma", "Dieci anni fissi", "Sei mesi non rinnovabili", "Tutta la carriera",
     "A", "La ferma iniziale di un VFI dura tipicamente un anno, con possibilità di rafferma successiva."),

    ("Carabinieri", "Diritto e ordinamento giudiziario",
     "Cosa si intende per 'flagranza di reato'?",
     "Un reato commesso molti anni prima", "Quando il reato viene commesso o è appena stato commesso e l'autore è colto sul fatto", "Un reato solo ipotizzato", "Un reato depenalizzato",
     "B", "Si ha flagranza quando il reo viene colto nell'atto di commettere il reato o subito dopo, con inseguimento o tracce evidenti."),
    ("Carabinieri", "Diritto e ordinamento giudiziario",
     "Chi redige il verbale di arresto in flagranza?",
     "Il Giudice", "L'ufficiale o agente di polizia giudiziaria che ha eseguito l'arresto", "L'avvocato difensore", "Il Sindaco",
     "B", "Il verbale di arresto viene redatto dall'ufficiale o agente di polizia giudiziaria che ha proceduto materialmente all'arresto."),
    ("Carabinieri", "Diritto e ordinamento giudiziario",
     "Cos'è il Codice di Procedura Penale?",
     "L'insieme delle norme che regolano lo svolgimento del processo penale", "Il regolamento interno dell'Arma", "Una raccolta di sentenze", "Il codice della strada",
     "A", "Il Codice di Procedura Penale disciplina le regole e le fasi del processo penale in Italia."),
    ("Carabinieri", "Diritto e ordinamento giudiziario",
     "Quale organo giudica in appello le sentenze di primo grado?",
     "La Corte di Cassazione", "La Corte d'Appello", "Il Tribunale Amministrativo Regionale", "Il Giudice di Pace",
     "B", "La Corte d'Appello è il giudice di secondo grado che riesamina le sentenze di primo grado."),
    ("Carabinieri", "Diritto e ordinamento giudiziario",
     "Cosa significa il principio di 'presunzione di innocenza'?",
     "L'imputato è considerato colpevole fino a prova contraria", "L'imputato si considera non colpevole fino a condanna definitiva", "Si applica solo ai minorenni", "Vale solo in appello",
     "B", "L'art. 27 Cost. sancisce che l'imputato non è considerato colpevole fino alla condanna definitiva."),
    ("Carabinieri", "Diritto e ordinamento giudiziario",
     "Chi rappresenta l'accusa in un processo penale italiano?",
     "L'avvocato della vittima", "Il Pubblico Ministero", "Il Giudice", "Il testimone principale",
     "B", "Il Pubblico Ministero rappresenta l'accusa e ha la titolarità dell'azione penale."),
    ("Carabinieri", "Diritto e ordinamento giudiziario",
     "Cos'è la Corte di Cassazione?",
     "Un tribunale di primo grado", "Il giudice di legittimità che verifica la corretta applicazione della legge, non il merito dei fatti", "Un organo amministrativo regionale", "L'organo che approva le leggi",
     "B", "La Cassazione è il giudice di legittimità: verifica che la legge sia stata applicata correttamente, senza riesaminare i fatti nel merito."),

    ("Guardia di Finanza", "Economia e finanza pubblica",
     "Cos'è il PIL (Prodotto Interno Lordo)?",
     "Il debito pubblico di uno Stato", "Il valore totale dei beni e servizi prodotti in un Paese in un anno", "Il totale delle tasse riscosse", "Il bilancio dello Stato",
     "B", "Il PIL misura il valore complessivo dei beni e servizi finali prodotti in un'economia in un dato periodo, di solito un anno."),
    ("Guardia di Finanza", "Economia e finanza pubblica",
     "Cosa si intende per inflazione?",
     "La diminuzione generale dei prezzi", "L'aumento generalizzato e continuo dei prezzi nel tempo", "L'aumento delle tasse", "La crescita del PIL",
     "B", "L'inflazione è l'aumento generalizzato e persistente del livello dei prezzi in un'economia."),
    ("Guardia di Finanza", "Economia e finanza pubblica",
     "Qual è la funzione principale di una dogana?",
     "Emettere passaporti", "Controllare e tassare le merci in entrata/uscita da un territorio doganale", "Gestire il traffico aereo", "Regolare i mutui bancari",
     "B", "La dogana controlla e applica i tributi sulle merci che attraversano i confini di un territorio doganale."),
    ("Guardia di Finanza", "Economia e finanza pubblica",
     "Cosa indica l'acronimo IRPEF?",
     "Imposta Regionale sulla Produzione", "Imposta sul Reddito delle Persone Fisiche", "Imposta sui Redditi da Pensione", "Imposta sulle Rendite Finanziarie",
     "B", "IRPEF sta per Imposta sul Reddito delle Persone Fisiche, la principale imposta diretta italiana sui redditi individuali."),
    ("Guardia di Finanza", "Economia e finanza pubblica",
     "Cos'è il riciclaggio di denaro?",
     "Il pagamento regolare delle tasse", "Il processo di occultare l'origine illecita di capitali per farli apparire legittimi", "Un tipo di investimento in borsa", "Una sanzione amministrativa",
     "B", "Il riciclaggio consiste nel far apparire lecita la provenienza di denaro ottenuto illecitamente."),
    ("Guardia di Finanza", "Economia e finanza pubblica",
     "Cosa si intende comunemente per 'paradiso fiscale'?",
     "Una zona economica speciale dell'UE", "Una giurisdizione con bassa tassazione e scarsa trasparenza, talvolta usata per eludere/evadere il fisco", "Un fondo pensione statale", "Un tipo di titolo di Stato",
     "B", "I paradisi fiscali sono giurisdizioni a bassa tassazione e ridotta trasparenza, talvolta sfruttate per pratiche fiscali abusive o illecite."),
    ("Guardia di Finanza", "Economia e finanza pubblica",
     "Quale istituto vigila sulla stabilità del sistema bancario italiano?",
     "L'INPS", "La Banca d'Italia", "L'Istat", "La Consob (da sola)",
     "B", "La Banca d'Italia, insieme alla BCE nell'ambito della vigilanza unica europea, vigila sulla stabilità del sistema bancario."),

    ("Esercito/Marina/Aeronautica", "Gradi e ordinamento militare",
     "Qual è il grado immediatamente superiore a Sergente nell'Esercito Italiano?",
     "Caporal Maggiore", "Sergente Maggiore", "Maresciallo Ordinario", "Tenente",
     "B", "Il Sergente Maggiore è il grado immediatamente superiore a Sergente nella gerarchia dei sottufficiali dell'Esercito."),
    ("Esercito/Marina/Aeronautica", "Gradi e ordinamento militare",
     "Come si chiama l'Accademia Militare che forma gli ufficiali dell'Esercito Italiano?",
     "Accademia Navale di Livorno", "Accademia Militare di Modena", "Accademia Aeronautica di Pozzuoli", "Scuola Ufficiali Carabinieri",
     "B", "L'Accademia Militare di Modena è l'istituto di formazione degli ufficiali dell'Esercito Italiano."),
    ("Esercito/Marina/Aeronautica", "Gradi e ordinamento militare",
     "Quale grado della Marina Militare corrisponde approssimativamente a 'Colonnello' dell'Esercito?",
     "Capitano di Fregata", "Capitano di Vascello", "Ammiraglio di Squadra", "Guardiamarina",
     "B", "Il Capitano di Vascello è il grado della Marina corrispondente approssimativamente al Colonnello dell'Esercito."),
    ("Esercito/Marina/Aeronautica", "Gradi e ordinamento militare",
     "Quale accademia forma gli ufficiali dell'Aeronautica Militare?",
     "Accademia Militare di Modena", "Accademia Navale di Livorno", "Accademia Aeronautica di Pozzuoli", "Scuola di Applicazione di Torino",
     "C", "L'Accademia Aeronautica, con sede a Pozzuoli, forma gli ufficiali dell'Aeronautica Militare."),
    ("Esercito/Marina/Aeronautica", "Gradi e ordinamento militare",
     "Dove ha sede l'Accademia Navale che forma gli ufficiali della Marina Militare?",
     "Taranto", "La Spezia", "Livorno", "Napoli",
     "C", "L'Accademia Navale ha sede a Livorno."),
    ("Esercito/Marina/Aeronautica", "Gradi e ordinamento militare",
     "Cosa indica colloquialmente il termine 'naia'?",
     "Un'unità navale", "Il servizio di leva obbligatorio, oggi sospeso", "Un tipo di addestramento fisico", "Un grado militare",
     "B", "'Naia' è il termine colloquiale con cui si indicava il servizio di leva obbligatorio, sospeso dal 2005."),
    ("Esercito/Marina/Aeronautica", "Gradi e ordinamento militare",
     "Quale grado della truppa nell'Aeronautica Militare è superiore ad 'Aviere semplice'?",
     "Aviere Scelto", "Maresciallo", "Sergente", "Generale di Squadra Aerea",
     "A", "L'Aviere Scelto è un grado della truppa superiore rispetto ad Aviere semplice nell'Aeronautica Militare."),
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
            valori = {**b, "stima_periodo_da": b.get("stima_periodo_da"), "stima_periodo_a": b.get("stima_periodo_a")}
            db.execute(
                """INSERT INTO bandi
                (corpo, categoria, titolo, posti, descrizione, testo_indicizzato,
                 data_pubblicazione, data_apertura, data_scadenza, stimato, fonte_url, fonte_tipo, note,
                 stima_periodo_da, stima_periodo_a)
                VALUES (:corpo, :categoria, :titolo, :posti, :descrizione, :testo_indicizzato,
                 :data_pubblicazione, :data_apertura, :data_scadenza, :stimato, :fonte_url, :fonte_tipo, :note,
                 :stima_periodo_da, :stima_periodo_a)""",
                valori,
            )
    # Inserimento incrementale (non solo "se la tabella è vuota"): ogni domanda
    # viene aggiunta una sola volta, verificando il testo esatto. Così le nuove
    # domande aggiunte in futuro arrivano anche su un database già popolato,
    # senza bisogno di svuotarlo.
    for q in QUIZ_QUESTIONS:
        domanda = q[1]
        esiste = db.execute("SELECT 1 FROM quiz_questions WHERE domanda = ?", (domanda,)).fetchone()
        if not esiste:
            db.execute(
                """INSERT INTO quiz_questions
                (materia, domanda, opzione_a, opzione_b, opzione_c, opzione_d, risposta, spiegazione)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                q,
            )
    for q in QUIZ_QUESTIONS_CORPO:
        corpo_specifico, materia, domanda, a, b_, c, d, risposta, spiegazione = q
        esiste = db.execute("SELECT 1 FROM quiz_questions WHERE domanda = ?", (domanda,)).fetchone()
        if not esiste:
            db.execute(
                """INSERT INTO quiz_questions
                (materia, domanda, opzione_a, opzione_b, opzione_c, opzione_d, risposta, spiegazione,
                 fonte, corpo_specifico)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'ad_hoc_su_materie_ufficiali', ?)""",
                (materia, domanda, a, b_, c, d, risposta, spiegazione, corpo_specifico),
            )
    if db.execute("SELECT COUNT(*) FROM checklist_template").fetchone()[0] == 0:
        for i, testo in enumerate(CHECKLIST_TEMPLATE):
            db.execute(
                "INSERT INTO checklist_template (testo, ordine) VALUES (?, ?)", (testo, i)
            )
    db.commit()
