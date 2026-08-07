import datetime
import json
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="MY FINANCE PRO", page_icon="💰", layout="centered"
)

# Inizializzazione dello Stato (Database Locale in Session State)
if "lingua" not in st.session_state:
    st.session_state.lingua = "it"
if "valuta" not in st.session_state:
    st.session_state.valuta = "EUR"

if "categorie_entrata" not in st.session_state:
    st.session_state.categorie_entrata = [
        "Stipendio / Pensione",
        "Bonus / Premi / Tredicesima",
        "Lavoro Autonomo / Extra",
        "Rendite / Investimenti",
        "Rimborsi / Sussidi",
        "Altre Entrate",
    ]

if "categorie_uscita" not in st.session_state:
    st.session_state.categorie_uscita = [
        "Affitto / Mutuo",
        "Utenze (Luce, Gas, Acqua)",
        "Internet e Telefonia",
        "Manutenzione e Arredo",
        "Supermercato / Alimentari",
        "Ristoranti / Bar / Take-away",
        "Carburante / Ricarica EV",
        "Assicurazione e Bollo",
        "Manutenzione Auto/Mezzi",
        "Mezzi Pubblici / Viaggi",
        "Farmacia e Visite Mediche",
        "Cura Personale / Sport",
        "Hobby e Intrattenimento",
        "Abbonamenti e Streaming",
        "Shopping e Abbigliamento",
        "Tasse e Imposte",
        "Prestiti / Rate / Finanziamenti",
        "Scuola e Figli",
        "Regali e Donazioni",
        "Altre Uscite / Imprevisti",
    ]

if "conti" not in st.session_state:
    st.session_state.conti = [
        {
            "id": "c1",
            "nome": "Conto Corrente Principale",
            "saldoIniziale": 1500.0,
            "valuta": "EUR",
            "isFinanziamento": False,
        },
        {
            "id": "c2",
            "nome": "Carta di Credito",
            "saldoIniziale": 0.0,
            "valuta": "EUR",
            "isFinanziamento": True,
        },
    ]

if "movimenti" not in st.session_state:
    st.session_state.movimenti = []

# Dizionario dei testi multilingua
dizionario = {
    "it": {
        "appTitle": "MY FINANCE PRO",
        "dash": "Dashboard",
        "list": "Movimenti",
        "report": "Report & Cash Flow",
        "settings": "Impostazioni",
        "realBalance": "SALDO LIQUIDO REALE (CONTI)",
        "loansBalance": "TOTALE DEBITI / FINANZIAMENTI",
        "yourAccounts": "I TUOI CONTI E CARTE",
        "addAccount": "Aggiungi Nuovo Conto",
        "newMov": "Nuovo Movimento",
        "selectAccount": "Seleziona Conto",
        "category": "Categoria (Obbligatoria)",
        "what": "Descrizione",
        "amount": "Importo",
        "save": "SALVA",
        "cancel": "ANNULLA",
        "delete": "ELIMINA",
        "settingsSaved": "Impostazioni salvate!",
        "lang": "Lingua App",
        "curr": "Valuta di Visualizzazione",
        "expenses": "Uscite",
        "incomes": "Entrate",
        "accountName": "Nome Conto",
        "initialBalance": "Saldo Iniziale",
        "isLoan": "Finanziamento / Carta Credito (Plafond)",
        "deleteAccount": "Elimina Conto",
    },
    "en": {
        "appTitle": "MY FINANCE PRO",
        "dash": "Dashboard",
        "list": "Transactions",
        "report": "Report & Cash Flow",
        "settings": "Settings",
        "realBalance": "NET LIQUID BALANCE (ACCOUNTS)",
        "loansBalance": "TOTAL LIABILITIES / CARDS",
        "yourAccounts": "YOUR ACCOUNTS & CARDS",
        "addAccount": "Add New Account",
        "newMov": "New Transaction",
        "selectAccount": "Select Account",
        "category": "Category (Required)",
        "what": "Description",
        "amount": "Amount",
        "save": "SAVE",
        "cancel": "CANCEL",
        "delete": "DELETE",
        "settingsSaved": "Settings saved!",
        "lang": "App Language",
        "curr": "Display Currency",
        "expenses": "Expenses",
        "incomes": "Incomes",
        "accountName": "Account Name",
        "initialBalance": "Initial Balance",
        "isLoan": "Loan / Credit Card (Plafond)",
        "deleteAccount": "Delete Account",
    },
}

tassiDiCambio = {"EUR": 1.0, "USD": 1.08, "GBP": 0.85, "CHF": 0.96, "JPY": 165.0}
simboliValuta = {"EUR": "€", "USD": "$", "GBP": "£", "CHF": "CHF", "JPY": "¥"}


def t(key):
    lang = st.session_state.lingua
    if lang in dizionario and key in dizionario[lang]:
        return dizionario[lang][key]
    return dizionario["en"].get(key, key)


def converti(importo, orig, dest):
    if orig == dest:
        return importo
    t_orig = tassiDiCambio.get(orig, 1.0)
    t_dest = tassiDiCambio.get(dest, 1.0)
    return (importo / t_orig) * t_dest


# --- BARRA LATERALE (MENU) ---
st.sidebar.title(t("appTitle"))
menu = st.sidebar.radio(
    "Navigazione", [t("dash"), t("list"), t("report"), t("settings")]
)

# --- SEZIONE: DASHBOARD ---
if menu == t("dash"):
    st.title(t("appTitle"))

    valuta_vis = st.session_state.valuta
    simbolo = simboliValuta.get(valuta_vis, "€")

    saldo_liquido = 0.0
    saldo_debiti = 0.0

    for c in st.session_state.conti:
        movs_conto = sum(
            m["v"]
            for m in st.session_state.movimenti
            if m["contoId"] == c["id"]
        )
        tot_nativo = c["saldoIniziale"] + movs_conto
        tot_conv = converti(tot_nativo, c["valuta"], valuta_vis)

        if c["isFinanziamento"]:
            saldo_debiti += tot_conv
        else:
            saldo_liquido += tot_conv

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=t("realBalance"), value=f"{saldo_liquido:,.2f} {simbolo}")
    with col2:
        st.metric(label=t("loansBalance"), value=f"{saldo_debiti:,.2f} {simbolo}")

    st.divider()
    st.subheader(t("yourAccounts"))

    for c in st.session_state.conti:
        movs_conto = sum(
            m["v"]
            for m in st.session_state.movimenti
            if m["contoId"] == c["id"]
        )
        tot_nativo = c["saldoIniziale"] + movs_conto
        c_simbolo = simboliValuta.get(c["valuta"], "€")
        st.write(
            f"💳 **{c['nome']}**: {tot_nativo:,.2f} {c_simbolo}"
            + (" (Finanziamento)" if c["isFinanziamento"] else "")
        )

# --- SEZIONE: MOVIMENTI ---
elif menu == t("list"):
    st.subheader(t("list"))

    # Form per aggiungere un movimento
    with st.form("nuovo_movimento_form"):
        st.write(t("newMov"))
        tipo_form = st.radio(
            "Tipo", [t("expenses"), t("incomes")], horizontal=True
        )

        if not st.session_state.conti:
            st.warning("Crea prima un conto nella sezione Impostazioni.")
            conto_sel_id = None
        else:
            conti_nomi = {c["id"]: c["nome"] for c in st.session_state.conti}
            conto_sel_id = st.selectbox(
                t("selectAccount"),
                options=list(conti_nomi.keys()),
                format_func=lambda x: conti_nomi[x],
            )

        cat_lista = (
            st.session_state.categorie_entrata
            if tipo_form == t("incomes")
            else st.session_state.categorie_uscita
        )
        cat_sel = st.selectbox(t("category"), options=cat_lista)

        descrizione = st.text_input(t("what"))
        importo = st.number_input(t("amount"), min_value=0.0, step=0.01)

        submitted = st.form_submit_button(t("save"))
        if submitted and conto_sel_id:
            valore_finale = -abs(importo) if tipo_form == t("expenses") else abs(importo)
            nuovo_mov = {
                "id": str(datetime.datetime.now().timestamp()),
                "contoId": conto_sel_id,
                "t": descrizione,
                "categoria": cat_sel,
                "v": valore_finale,
                "data": datetime.date.today().isoformat(),
            }
            st.session_state.movimenti.append(nuovo_mov)
            st.success("Movimento salvato con successo!")

    st.divider()
    st.write("### Elenco Movimenti")
    if not st.session_state.movimenti:
        st.info("Nessun movimento trovato.")
    else:
        for idx, m in enumerate(reversed(st.session_state.movimenti)):
            c_nome = next(
                (c["nome"] for c in st.session_state.conti if c["id"] == m["contoId"]),
                "Conto",
            )
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.write(
                    f"📅 {m['data']} | **{c_nome}** | {m['categoria']} - {m['t']} | "
                    f"**{m['v']:,.2f}**"
                )
            with col_b:
                if st.button("🗑️", key=f"del_mov_{m['id']}"):
                    st.session_state.movimenti = [
                        item for item in st.session_state.movimenti if item["id"] != m["id"]
                    ]
                    st.rerun()

# --- SEZIONE: REPORT & CASH FLOW ---
elif menu == t("report"):
    st.subheader(t("report"))

    if not st.session_state.movimenti:
        st.info("Nessun movimento registrato per generare i report.")
    else:
        tot_entrate = sum(m["v"] for m in st.session_state.movimenti if m["v"] > 0)
        tot_uscite = sum(abs(m["v"]) for m in st.session_state.movimenti if m["v"] < 0)
        cash_flow_netto = tot_entrate - tot_uscite

        valuta_vis = st.session_state.valuta
        simbolo = simboliValuta.get(valuta_vis, "€")

        col1, col2, col3 = st.columns(3)
        col1.metric("Totale Entrate", f"{tot_entrate:,.2f} {simbolo}")
        col2.metric("Totale Uscite", f"{tot_uscite:,.2f} {simbolo}")
        col3.metric("Cash Flow Netto", f"{cash_flow_netto:,.2f} {simbolo}")

        st.divider()
        st.subheader("Uscite per Categoria")
        spese_per_cat = {}
        for m in st.session_state.movimenti:
            if m["v"] < 0:
                cat = m["categoria"]
                spese_per_cat[cat] = spese_per_cat.get(cat, 0.0) + abs(m["v"])

        if spese_per_cat:
            for cat, importo in sorted(spese_per_cat.items(), key=lambda x: x[1], reverse=True):
                st.write(f"- **{cat}**: {importo:,.2f} {simbolo}")
        else:
            st.write("Nessuna spesa registrata.")

# --- SEZIONE: IMPOSTAZIONI & GESTIONE CONTI ---
elif menu == t("settings"):
    st.subheader(t("settings"))

    # Config lingua e valuta
    lingua_scelta = st.selectbox(
        t("lang"),
        options=["it", "en"],
        index=0 if st.session_state.lingua == "it" else 1,
    )
    valuta_scelta = st.selectbox(
        t("curr"),
        options=list(tassiDiCambio.keys()),
        index=list(tassiDiCambio.keys()).index(st.session_state.valuta),
    )

    if st.button(t("save")):
        st.session_state.lingua = lingua_scelta
        st.session_state.valuta = valuta_scelta
        st.success(t("settingsSaved"))
        st.rerun()

    st.divider()
    st.subheader("Gestione Conti e Carte")

    # Form per aggiungere un nuovo conto
    with st.form("nuovo_conto_form"):
        st.write(t("addAccount"))
        nome_nuovo_conto = st.text_input(t("accountName"))
        saldo_iniziale_nuovo = st.number_input(t("initialBalance"), value=0.0, step=0.01)
        valuta_nuovo_conto = st.selectbox("Valuta Conto", options=list(tassiDiCambio.keys()))
        is_finanziamento_nuovo = st.checkbox(t("isLoan"))

        aggiungi_conto_sub = st.form_submit_button("Crea Conto")
        if aggiungi_conto_sub and nome_nuovo_conto:
            nuovo_id = "c_" + str(datetime.datetime.now().timestamp())
            st.session_state.conti.append({
                "id": nuovo_id,
                "nome": nome_nuovo_conto,
                "saldoIniziale": saldo_iniziale_nuovo,
                "valuta": valuta_nuovo_conto,
                "isFinanziamento": is_finanziamento_nuovo
            })
            st.success(f"Conto '{nome_nuovo_conto}' aggiunto con successo!")
            st.rerun()

    st.write("### Conti Esistenti (Elimina)")
    for c in st.session_state.conti:
        col_c1, col_c2 = st.columns([3, 1])
        with col_c1:
            st.write(f"💳 **{c['nome']}** ({c['valuta']})")
        with col_c2:
            if st.button(t("delete"), key=f"del_conto_{c['id']}"):
                if len(st.session_state.conti) <= 1:
                    st.error("Non puoi eliminare l'ultimo conto rimasto!")
                else:
                    # Rimuove il conto e i movimenti associati
                    st.session_state.conti = [item for item in st.session_state.conti if item["id"] != c["id"]]
                    st.session_state.movimenti = [m for m in st.session_state.movimenti if m["contoId"] != c["id"]]
                    st.success("Conto eliminato.")
                    st.rerun()
