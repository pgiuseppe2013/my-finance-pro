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
        "settings": "Impostazioni",
        "realBalance": "SALDO LIQUIDO REALE (CONTI)",
        "loansBalance": "TOTALE DEBITI / FINANZIAMENTI",
        "yourAccounts": "I TUOI CONTI E CARTE",
        "addAccount": "Aggiungi Conto",
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
    },
    "en": {
        "appTitle": "MY FINANCE PRO",
        "dash": "Dashboard",
        "list": "Transactions",
        "settings": "Settings",
        "realBalance": "NET LIQUID BALANCE (ACCOUNTS)",
        "loansBalance": "TOTAL LIABILITIES / CARDS",
        "yourAccounts": "YOUR ACCOUNTS & CARDS",
        "addAccount": "Add Account",
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
    "Navigazione", [t("dash"), t("list"), t("settings")]
)

# --- SEZIONE: DASHBOARD ---
if menu == t("dash"):
  st.title(t("appTitle"))

  # Calcolo Saldi
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
    if submitted:
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
    for m in reversed(st.session_state.movimenti):
      c_nome = next(
          (c["nome"] for c in st.session_state.conti if c["id"] == m["contoId"]),
          "Conto",
      )
      st.write(
          f"📅 {m['data']} | **{c_nome}** | {m['categoria']} - {m['t']} | "
          f"**{m['v']:,.2f}**"
      )

# --- SEZIONE: IMPOSTAZIONI ---
elif menu == t("settings"):
  st.subheader(t("settings"))

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
