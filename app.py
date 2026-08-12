import streamlit as st
import pandas as pd
import datetime
from datetime import date, timedelta
import plotly.express as px

# 1. CONFIGURAZIONE PAGINA & STILE DARK PROFONDO
st.set_page_config(page_title="MY FINANCE PRO", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #cbd5e1; }
    .stButton>button {
        border-radius: 8px;
        background: linear-gradient(145deg, #0f172a, #1e293b);
        color: #f8fafc;
        border: 1px solid #334155;
        padding: 8px 16px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(145deg, #1e293b, #334155);
        border-color: #22c55e;
        color: #22c55e;
    }
    div[data-testid="stMetricValue"] { color: #22c55e; font-family: 'Urbanist', sans-serif; font-weight: 700; }
    .stDateInput input, .stTextInput input, .stNumberInput input { background-color: #0f172a !important; color: #f8fafc !important; border: 1px solid #334155 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. INIZIALIZZAZIONE STATO
if 'accounts' not in st.session_state:
    st.session_state.accounts = []
if 'movements' not in st.session_state:
    st.session_state.movements = []
if 'settings' not in st.session_state:
    st.session_state.settings = {"lang": "IT", "currency": "EUR"}
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "DASHBOARD"

if 'cats_in' not in st.session_state:
    st.session_state.cats_in = ["Stipendio", "Rendita", "Bonus", "Vendita", "Altro"]
if 'cats_out' not in st.session_state:
    st.session_state.cats_out = ["Affitto", "Mutuo", "Utenze", "Supermercato", "Shopping", "Trasporti", "Salute", "Svago"]

# 3. DIZIONARIO TRADUZIONI MULTILINGUA COMPLETO
TRANSLATIONS = {
    "IT": {
        "title": "⚡ MY FINANCE PRO",
        "dash": "📊 DASHBOARD",
        "mov": "📝 MOVIMENTI",
        "rep": "📈 REPORT & CASH FLOW",
        "set": "⚙️ IMPOSTAZIONI",
        "tot_liq": "LIQUIDITÀ TOTALE",
        "panoramica": "Panoramica Patrimoniale e Conti",
        "add_acc": "➕ Aggiungi Nuovo Conto o Carta",
        "type_acc": "Tipo di Rapporto",
        "name_acc": "Nome Conto / Carta",
        "init_bal": "Saldo di Partenza",
        "init_date": "A che data hai questo saldo?",
        "plafond": "Plafond Mensile",
        "scad_carta": "Data Scadenza Carta",
        "giorno_add": "Giorno Addebito",
        "btn_create_acc": "CREA CONTO / CARTA",
        "succ_acc": "✅ Conto o carta inserito con successo!",
        "add_mov": "➕ Aggiungi Nuovo Movimento",
        "data_cont": "Data Contabile",
        "data_val": "Data Valuta",
        "sel_acc": "Seleziona Conto / Carta",
        "op_type": "Tipo Operazione",
        "entrata": "Entrata",
        "uscita": "Uscita",
        "cat": "Categoria",
        "importo": "Importo",
        "desc": "Descrizione (Opzionale)",
        "repeat": "Ripeti movimento nel tempo",
        "freq": "Frequenza",
        "mensile": "Mensile",
        "annuale": "Annuale",
        "num_rip": "Numero di ripetizioni",
        "btn_reg_mov": "REGISTRA MOVIMENTO",
        "succ_mov": "✅ Movimento inserito con successo!",
        "search_mov": "🔍 Cerca nei movimenti...",
        "gest_mov": "Gestione e Modifica Movimenti",
        "analisi_cf": "Analisi Cash Flow e Dettagli",
        "sel_periodo": "Seleziona Periodo Analisi (Passato & Futuro)",
        "trend_cf": "Trend Cash Flow Patrimoniale (Incluso Saldo Iniziale Banca)",
        "dett_cat": "📊 Schema Cash Flow per Macrovoci",
        "vista_dett": "Fissa vista dettaglio:",
        "tutti": "Tutti",
        "solo_ent": "Solo Entrate",
        "solo_usc": "Solo Uscite",
        "config_app": "⚙️ Configurazioni App",
        "gest_cat": "📁 Gestisci Classificazione Categorie",
        "pref_ling": "🌐 Preferenze Lingua e Valuta",
        "lingua": "Lingua",
        "valuta": "Valuta",
        "btn_salva_set": "SALVA IMPOSTAZIONI",
        "succ_set": "✅ Impostazioni salvate con successo!",
        "del_conto": "Elimina Conto",
        "residuo_plaf": "Residuo Plafond",
        "scadenza": "Scadenza",
        "warning_no_acc": "⚠️ Crea prima almeno un Conto o una Carta di Credito dalla Dashboard per poter inserire movimenti.",
        "err_name_acc": "Inserisci un nome valido per il conto."
    },
    "EN": {
        "title": "⚡ MY FINANCE PRO",
        "dash": "📊 DASHBOARD",
        "mov": "📝 TRANSACTIONS",
        "rep": "📈 REPORT & CASH FLOW",
        "set": "⚙️ SETTINGS",
        "tot_liq": "TOTAL LIQUIDITY",
        "panoramica": "Asset Overview & Accounts",
        "add_acc": "➕ Add New Account or Card",
        "type_acc": "Account Type",
        "name_acc": "Account / Card Name",
        "init_bal": "Initial Balance",
        "init_date": "As of what date is this balance?",
        "plafond": "Monthly Limit",
        "scad_carta": "Card Expiry Date",
        "giorno_add": "Charge Day",
        "btn_create_acc": "CREATE ACCOUNT / CARD",
        "succ_acc": "✅ Account or card successfully created!",
        "add_mov": "➕ Add New Transaction",
        "data_cont": "Accounting Date",
        "data_val": "Value Date",
        "sel_acc": "Select Account / Card",
        "op_type": "Operation Type",
        "entrata": "Income",
        "uscita": "Expense",
        "cat": "Category",
        "importo": "Amount",
        "desc": "Description (Optional)",
        "repeat": "Repeat transaction over time",
        "freq": "Frequency",
        "mensile": "Monthly",
        "annuale": "Yearly",
        "num_rip": "Number of repetitions",
        "btn_reg_mov": "REGISTER TRANSACTION",
        "succ_mov": "✅ Transaction successfully registered!",
        "search_mov": "🔍 Search transactions...",
        "gest_mov": "Transactions Management & Editing",
        "analisi_cf": "Cash Flow Analysis & Details",
        "sel_periodo": "Select Analysis Period (Passato & Futuro)",
        "trend_cf": "Patrimonial Cash Flow Trend (Incl. Bank Initial Balance)",
        "dett_cat": "📊 Cash Flow Macro-Categories Scheme",
        "vista_dett": "Filter detail view:",
        "tutti": "All",
        "solo_ent": "Only Income",
        "solo_usc": "Only Expenses",
        "config_app": "⚙️ App Configurations",
        "gest_cat": "📁 Manage Category Classification",
        "pref_ling": "🌐 Language & Currency Preferences",
        "lingua": "Language",
        "valuta": "Currency",
        "btn_salva_set": "SAVE SETTINGS",
        "succ_set": "✅ Settings successfully saved!",
        "del_conto": "Delete Account",
        "residuo_plaf": "Remaining Limit",
        "scadenza": "Expiry",
        "warning_no_acc": "⚠️ Please create at least one Account or Credit Card from the Dashboard first.",
        "err_name_acc": "Please enter a valid account name."
    },
    "FR": {
        "title": "⚡ MY FINANCE PRO",
        "dash": "📊 TABLEAU DE BORD",
        "mov": "📝 TRANSACTIONS",
        "rep": "📈 RAPPORT & FLUX DE TRÉSORERIE",
        "set": "⚙️ PARAMÈTRES",
        "tot_liq": "LIQUIDITÉ TOTALE",
        "panoramica": "Aperçu des Actifs & Comptes",
        "add_acc": "➕ Ajouter un Compte ou une Carte",
        "type_acc": "Type de Compte",
        "name_acc": "Nom du Compte / Carte",
        "init_bal": "Solde Initial",
        "init_date": "À quelle date avez-vous ce solde ?",
        "plafond": "Plafond Mensuel",
        "scad_carta": "Date d'Expiration de la Carte",
        "giorno_add": "Jour de Prélèvement",
        "btn_create_acc": "CRÉER COMPTE / CARTE",
        "succ_acc": "✅ Compte ou carte créé avec succès !",
        "add_mov": "➕ Ajouter une Transaction",
        "data_cont": "Date Comptable",
        "data_val": "Date de Valeur",
        "sel_acc": "Sélectionner Compte / Carte",
        "op_type": "Type d'Opération",
        "entrata": "Revenu",
        "uscita": "Dépense",
        "cat": "Catégorie",
        "importo": "Montant",
        "desc": "Description (Optionnel)",
        "repeat": "Répéter la transaction dans le temps",
        "freq": "Fréquence",
        "mensile": "Mensuel",
        "annuale": "Annuel",
        "num_rip": "Nombre de répétitions",
        "btn_reg_mov": "ENREGISTRER LA TRANSACTION",
        "succ_mov": "✅ Transaction enregistrée avec succès !",
        "search_mov": "🔍 Rechercher des transactions...",
        "gest_mov": "Gestion et Modification",
        "analisi_cf": "Analyse du Flux & Détails",
        "sel_periodo": "Sélectionner la Période (Passé & Futur)",
        "trend_cf": "Tendance du Flux (Solde Initial de Banque Inclus)",
        "dett_cat": "📊 Schéma des Flux par Macro-Catégories",
        "vista_dett": "Filtrer la vue:",
        "tutti": "Tous",
        "solo_ent": "Seulement Revenus",
        "solo_usc": "Seulement Dépenses",
        "config_app": "⚙️ Configuration de l'App",
        "gest_cat": "📁 Gérer les Catégories",
        "pref_ling": "🌐 Préférences de Langue & Devise",
        "lingua": "Langue",
        "valuta": "Devise",
        "btn_salva_set": "ENREGISTRER LES PARAMÈTRES",
        "succ_set": "✅ Paramètres enregistrés avec succès !",
        "del_conto": "Supprimer le Compte",
        "residuo_plaf": "Plafond Restant",
        "scadenza": "Expiration",
        "warning_no_acc": "⚠️ Veuillez d'abord créer un Compte ou une Carte.",
        "err_name_acc": "Veuillez entrer un nom valide."
    }
}

def t(key):
    lang = st.session_state.settings["lang"]
    if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
        return TRANSLATIONS[lang][key]
    return TRANSLATIONS["EN"].get(key, key)

LANGS = ["IT", "EN", "FR", "ES", "DE", "PT", "ZH", "JA", "RU", "AR"]
CURRS = ["EUR", "USD", "GBP", "CHF", "JPY", "CAD", "AUD", "CNY", "INR", "BRL"]

# 4. FUNZIONE LOGICA CALCOLO SALDO CON DATA DI CUT-OFF
def get_account_balance(acc):
    acc_id = acc['id']
    init_bal = acc['init_bal']
    init_date = acc.get('init_date', date.min)
    
    valid_movements = [
        m for m in st.session_state.movements 
        if m['acc_id'] == acc_id and not m.get('virtual') and pd.to_datetime(m['date_c']).date() >= init_date
    ]
    
    return init_bal + sum(m['amt'] for m in valid_movements)

# 5. FUNZIONE AGGIUNTA MOVIMENTO CON GESTIONE RIPETIZIONI NEL TEMPO
def add_movement(m_date_c, m_date_v, acc_id, m_type, cat, desc, amt, repeat=False, freq="Mensile", count=1):
    acc = next((a for a in st.session_state.accounts if a['id'] == acc_id), None)
    
    iterations = count if repeat else 1
    
    for i in range(iterations):
        if i == 0:
            curr_dc = m_date_c
            curr_dv = m_date_v
        else:
            if freq == "Mensile":
                try:
                    curr_dc = m_date_c.replace(day=1) + timedelta(days=32 * i)
                    curr_dc = curr_dc.replace(day=m_date_c.day)
                except ValueError:
                    curr_dc = m_date_c + timedelta(days=30 * i)
                try:
                    curr_dv = m_date_v.replace(day=1) + timedelta(days=32 * i)
                    curr_dv = curr_dv.replace(day=m_date_v.day)
                except ValueError:
                    curr_dv = m_date_v + timedelta(days=30 * i)
            else:
                try:
                    curr_dc = m_date_c.replace(year=m_date_c.year + i)
                except ValueError:
                    curr_dc = m_date_c + timedelta(days=365 * i)
                try:
                    curr_dv = m_date_v.replace(year=m_date_v.year + i)
                except ValueError:
                    curr_dv = m_date_v + timedelta(days=365 * i)

        if acc and acc['type'] == "Carta di Credito" and amt < 0:
            try:
                next_month = curr_dc.replace(day=1) + timedelta(days=32)
                addebito_date = next_month.replace(day=acc.get('addebito_day', 1))
            except ValueError:
                addebito_date = curr_dc + timedelta(days=30)
                
            st.session_state.movements.append({
                "id": f"PREV_{datetime.datetime.now().timestamp()}_{i}",
                "date_c": addebito_date, "date_v": addebito_date,
                "acc_id": acc_id, "type": "Uscita (Prev)", "cat": "Saldo Carta",
                "desc": f"Addebito carta: {desc}" if not desc else f"Addebito carta: {desc} ({i+1})", "amt": amt, "virtual": True
            })
        
        st.session_state.movements.append({
            "id": f"{datetime.datetime.now().timestamp()}_{i}",
            "date_c": curr_dc, "date_v": curr_dv,
            "acc_id": acc_id, "type": m_type, "cat": cat,
            "desc": desc if i == 0 else f"{desc} ({i+1})" if desc else f"Ripetizione {i+1}", "amt": amt, "virtual": False
        })

# 6. WIDGET MOVIMENTO DIETRO "+" CON PULIZIA TOTALE FORM AL SUCCESS
def render_movement_form(key_suffix=""):
    with st.expander(t("add_mov")):
        if not st.session_state.accounts:
            st.warning(t("warning_no_acc"))
            return

        dc_key = f"dc_input_{key_suffix}"
        dv_key = f"dv_input_{key_suffix}"
        last_dc_key = f"last_dc_{key_suffix}"
        
        if dc_key not in st.session_state:
            st.session_state[dc_key] = date.today()
        if dv_key not in st.session_state:
            st.session_state[dv_key] = date.today()
        if last_dc_key not in st.session_state:
            st.session_state[last_dc_key] = st.session_state[dc_key]

        col1, col2, col3 = st.columns(3)
        with col1:
            dc = st.date_input(t("data_cont"), key=dc_key)
            
        if dc != st.session_state[last_dc_key]:
            st.session_state[dv_key] = dc
            st.session_state[last_dc_key] = dc

        with col2:
            dv = st.date_input(t("data_val"), key=dv_key)
        with col3:
            acc_choice = st.selectbox(t("sel_acc"), [a['name'] for a in st.session_state.accounts], key=f"acc_sel_{key_suffix}")

        col4, col5, col6 = st.columns(3)
        with col4:
            m_type = st.radio(t("op_type"), [t("entrata"), t("uscita")], horizontal=True, key=f"m_type_{key_suffix}")
        with col5:
            is_income = (m_type == t("entrata"))
            cats = st.session_state.cats_in if is_income else st.session_state.cats_out
            cat = st.selectbox(t("cat"), cats, key=f"cat_{key_suffix}")
        with col6:
            amt = st.number_input(t("importo"), min_value=0.01, step=1.0, key=f"amt_{key_suffix}")
            if m_type == t("uscita"): amt = -amt

        desc = st.text_input(t("desc"), key=f"desc_{key_suffix}")

        repeat_check = st.checkbox(t("repeat"), key=f"repeat_chk_{key_suffix}")
        freq = "Mensile"
        count = 1
        if repeat_check:
            rc1, rc2 = st.columns(2)
            with rc1:
                freq = st.selectbox(t("freq"), [t("mensile"), t("annuale")], key=f"freq_sel_{key_suffix}")
                freq = "Mensile" if freq == t("mensile") else "Annuale"
            with rc2:
                count = st.number_input(t("num_rip"), min_value=2, max_value=60, value=12, key=f"count_sel_{key_suffix}")

        if st.button(t("btn_reg_mov"), key=f"btn_save_mov_{key_suffix}"):
            a_id = next(a['id'] for a in st.session_state.accounts if a['name'] == acc_choice)
            add_movement(dc, dv, a_id, m_type, cat, desc, amt, repeat=repeat_check, freq=freq, count=count)
            st.success(t("succ_mov"))
            for k in [dc_key, dv_key, f"amt_{key_suffix}", f"desc_{key_suffix}"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

# 7. BARRA DI NAVIGAZIONE A PULSANTI
st.title(t("title"))
b1, b2, b3, b4 = st.columns(4)
with b1:
    if st.button(t("dash"), use_container_width=True): st.session_state.active_tab = "DASHBOARD"
with b2:
    if st.button(t("mov"), use_container_width=True): st.session_state.active_tab = "MOVIMENTI"
with b3:
    if st.button(t("rep"), use_container_width=True): st.session_state.active_tab = "REPORT"
with b4:
    if st.button(t("set"), use_container_width=True): st.session_state.active_tab = "IMPOSTAZIONI"

st.divider()
menu = st.session_state.active_tab

# --- DASHBOARD ---
if menu == "DASHBOARD":
    st.subheader(t("panoramica"))
    
    total_cash = sum(get_account_balance(a) for a in st.session_state.accounts if a['type'] != "Carta di Credito")
    st.metric(t("tot_liq"), f"{total_cash:,.2f} {st.session_state.settings['currency']}")

    cols = st.columns(3)
    for i, acc in enumerate(st.session_state.accounts):
        with cols[i % 3]:
            with st.container(border=True):
                bal = get_account_balance(acc)
                st.markdown(f"### {acc['name']}")
                st.caption(f"Tipo: {acc['type']} | Dal: {acc.get('init_date', date.today()).strftime('%d/%m/%Y') if acc['type'] != 'Carta di Credito' else 'N/D'}")
                
                if acc['type'] == "Carta di Credito":
                    used = abs(sum(m['amt'] for m in st.session_state.movements if m['acc_id'] == acc['id'] and m['amt'] < 0 and not m.get('virtual')))
                    residuo = acc['plafond'] - used
                    st.metric(t("residuo_plaf"), f"{residuo:,.2f}")
                    st.caption(f"{t('scadenza')}: {acc.get('scadenza', 'N/D')}")
                    st.progress(residuo / acc['plafond'] if acc['plafond'] > 0 else 0)
                else:
                    st.metric("Saldo Attuale", f"{bal:,.2f}")
                
                if st.button(t("del_conto"), key=f"del_{acc['id']}"):
                    st.session_state.accounts = [a for a in st.session_state.accounts if a['id'] != acc['id']]
                    st.rerun()

    st.divider()

    with st.expander(t("add_acc")):
        t_acc = st.selectbox(t("type_acc"), ["Bancario", "Prepagata", "Carta di Credito"])
        name_acc_key = "acc_name_dash_input"
        name = st.text_input(t("name_acc"), key=name_acc_key)
        
        init = 0.0
        init_date = date.today()
        plafond = 0.0
        addebito = 1
        scadenza = date.today() + timedelta(days=365)
        
        if t_acc == "Carta di Credito":
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                plafond = st.number_input(t("plafond"), value=1500.0, step=100.0, key="acc_plafond_dash")
            with col_p2:
                scadenza = st.date_input(t("scad_carta"), value=scadenza, key="acc_scad_dash")
            with col_p3:
                addebito = st.slider(t("giorno_add"), 1, 28, 1, key="acc_add_dash")
        else:
            col_i1, col_i2 = st.columns(2)
            with col_i1:
                init = st.number_input(t("init_bal"), value=0.0, step=100.0, key="acc_init_dash")
            with col_i2:
                init_date = st.date_input(t("init_date"), value=date.today(), key="acc_init_date_dash")
        
        if st.button(t("btn_create_acc"), key="btn_create_acc_dash"):
            if name.strip() == "":
                st.warning(t("err_name_acc"))
            else:
                new_id = str(datetime.datetime.now().timestamp())
                st.session_state.accounts.append({
                    "id": new_id, "name": name, "type": t_acc, 
                    "init_bal": init, "init_date": init_date, 
                    "plafond": plafond, "addebito_day": addebito,
                    "scadenza": scadenza.strftime("%d/%m/%Y") if t_acc == "Carta di Credito" else ""
                })
                st.success(t("succ_acc"))
                if name_acc_key in st.session_state:
                    del st.session_state[name_acc_key]
                st.rerun()

# --- MOVIMENTI ---
elif menu == "MOVIMENTI":
    st.subheader(t("gest_mov"))
    render_movement_form(key_suffix="mov_tab")

    st.divider()
    search = st.text_input(t("search_mov"), key="search_mov")
    real_movs = [m for m in st.session_state.movements if not m.get('virtual')]
    if search:
        real_movs = [m for m in real_movs if search.lower() in m.get('desc', '').lower() or search.lower() in m.get('cat', '').lower()]

    if real_movs:
        st.markdown("### Elenco Movimenti Registrati")
        for m in real_movs:
            with st.container(border=True):
                c1, c2, c3, c4, c5, c6 = st.columns([2, 2, 2, 3, 2, 2])
                c1.text(str(m['date_c']))
                c2.text(m['type'])
                c3.text(m['cat'])
                c4.text(m['desc'] if m['desc'] else "-")
                c5.text(f"{m['amt']:,.2f}")
                
                b_col1, b_col2 = c6.columns(2)
                with b_col1:
                    if st.button("✏️", key=f"edit_btn_{m['id']}"):
                        st.session_state[f"editing_{m['id']}"] = True
                with b_col2:
                    if st.button("🗑️", key=f"del_btn_{m['id']}"):
                        st.session_state.movements = [item for item in st.session_state.movements if item['id'] != m['id']]
                        st.rerun()
                
                if st.session_state.get(f"editing_{m['id']}", False):
                    st.divider()
                    st.markdown(f"**Modifica Movimento:** {m['desc']}")
                    e_col1, e_col2, e_col3 = st.columns(3)
                    with e_col1:
                        new_dc = st.date_input("Data Contabile", value=pd.to_datetime(m['date_c']).date(), key=f"ed_dc_{m['id']}")
                    with e_col2:
                        new_cat = st.text_input("Categoria", value=m['cat'], key=f"ed_cat_{m['id']}")
                    with e_col3:
                        new_amt = st.number_input("Importo", value=float(m['amt']), step=1.0, key=f"ed_amt_{m['id']}")
                    new_desc = st.text_input("Descrizione", value=m['desc'], key=f"ed_desc_{m['id']}")
                    
                    sc1, sc2 = st.columns(2)
                    with sc1:
                        if st.button("Salva Modifiche", key=f"save_edit_{m['id']}"):
                            m['date_c'] = new_dc
                            m['date_v'] = new_dc
                            m['cat'] = new_cat
                            m['amt'] = new_amt
                            m['desc'] = new_desc
                            st.session_state[f"editing_{m['id']}"] = False
                            st.success("Modifiche salvate!")
                            st.rerun()
                    with sc2:
                        if st.button("Annulla", key=f"cancel_edit_{m['id']}"):
                            st.session_state[f"editing_{m['id']}"] = False
                            st.rerun()
    else:
        st.info("Nessun movimento registrato.")

# --- REPORT & CASH FLOW (SCHEMA PURO CON CONSUNTIVO EFFETTIVO) ---
elif menu == "REPORT":
    st.subheader(t("analisi_cf"))
    
    # RIMOSSO COMPLETAMENTE render_movement_form da qui (niente inserimento movimenti nella dash del cash flow)

    st.divider()
    d_range = st.date_input(t("sel_periodo"), [date.today() - timedelta(days=90), date.today() + timedelta(days=90)], key="report_range")
    
    if len(d_range) == 2:
        df = pd.DataFrame(st.session_state.movements)
        
        base_rows = []
        init_bank_total = 0.0
        for acc in st.session_state.accounts:
            if acc['type'] != "Carta di Credito":
                init_val = acc.get('init_bal', 0.0)
                init_bank_total += init_val
                base_rows.append({
                    "id": f"init_bank_{acc['id']}",
                    "date_c": acc.get('init_date', d_range[0]),
                    "date_v": acc.get('init_date', d_range[0]),
                    "acc_id": acc['id'],
                    "type": "Saldo Iniziale",
                    "cat": "Capitale Iniziale",
                    "desc": f"Saldo iniziale conto: {acc['name']}",
                    "amt": init_val,
                    "virtual": False
                })
        
        df_base = pd.DataFrame(base_rows) if base_rows else pd.DataFrame(columns=['id', 'date_c', 'date_v', 'acc_id', 'type', 'cat', 'desc', 'amt', 'virtual'])
        
        if not df.empty:
            df['date_c'] = pd.to_datetime(df['date_c']).dt.date
            df_combined = pd.concat([df_base, df], ignore_index=True)
        else:
            df_combined = df_base
            
        if not df_combined.empty:
            df_combined['date_c'] = pd.to_datetime(df_combined['date_c']).dt.date
            df_sorted = df_combined.sort_values('date_c').copy()
            df_sorted['cumulative_flow'] = df_sorted['amt'].cumsum()
            
            mask_period = (df_sorted['date_c'] >= d_range[0]) & (df_sorted['date_c'] <= d_range[1])
            df_filtered_period = df_sorted[mask_period]
            df_period_movements = df_filtered_period[df_filtered_period['type'] != "Saldo Iniziale"]
            
            # Distinzione tra movimenti schedulati (futuri/tutti) ed effettivamente REALIZZATI (fino ad oggi)
            today_date = date.today()
            df_realized = df_period_movements[pd.to_datetime(df_period_movements['date_c']).dt.date <= today_date]
            
            e_real = df_realized[df_realized['amt'] > 0]['amt'].sum()
            u_real = df_realized[df_realized['amt'] < 0]['amt'].sum()
            net_real = e_real + u_real
            
            # --- SEZIONE CONSUNTIVO EFFETTIVO ---
            st.markdown("### 📌 Resoconto di quanto effettivamente realizzato (Consuntivo ad oggi)")
            rc1, rc2, rc3 = st.columns(3)
            rc1.metric("Entrate Realizzate", f"{e_real:,.2f}")
            rc2.metric("Uscite Realizzate", f"{u_real:,.2f}")
            rc3.metric("Flusso Netto Realizzato", f"{net_real:,.2f}")
            
            st.divider()
            
            df_for_chart = df_sorted[df_sorted['date_c'] <= d_range[1]]
            
            fig = px.area(df_for_chart, x='date_c', y='cumulative_flow', title=t("trend_cf"), template="plotly_dark", labels={'cumulative_flow': 'Patrimonio Totale', 'date_c': 'Data'})
            fig.update_traces(line_color='#22c55e', fillcolor='rgba(34, 197, 94, 0.2)')
            st.plotly_chart(fig, use_container_width=True)
            
            # --- SCHEMA CASH FLOW PURO (SENZA TOTALI DI RIGA ESTERNI) ---
            st.markdown(f"### {t('dett_cat')}")
            
            summary_data = []
            
            # Riga del Saldo (Differenziata graficamente con etichetta dedicata)
            summary_data.append({
                "Schema Cash Flow (Macrovoci)": "+/- SALDO INIZIALE BANCA (Stock)",
                "Importo": init_bank_total
            })
            
            # Entrate
            for cat_in in st.session_state.cats_in:
                cat_sum = df_period_movements[(df_period_movements['cat'] == cat_in) & (df_period_movements['amt'] > 0)]['amt'].sum()
                summary_data.append({
                    "Schema Cash Flow (Macrovoci)": f"+ {cat_in}",
                    "Importo": cat_sum
                })
                
            # Uscite
            for cat_out in st.session_state.cats_out:
                cat_sum = df_period_movements[(df_period_movements['cat'] == cat_out) & (df_period_movements['amt'] < 0)]['amt'].sum()
                summary_data.append({
                    "Schema Cash Flow (Macrovoci)": f"- {cat_out}",
                    "Importo": cat_sum
                })
                
            df_summary = pd.DataFrame(summary_data)
            
            filter_mode = st.radio(t("vista_dett"), [t("tutti"), t("solo_ent"), t("solo_usc")], horizontal=True, key="filter_mode")
            if filter_mode == t("solo_ent"):
                df_summary_show = df_summary[df_summary['Schema Cash Flow (Macrovoci)'].str.contains("SALDO|\\+", case=False, regex=True)]
            elif filter_mode == t("solo_usc"):
                df_summary_show = df_summary[df_summary['Schema Cash Flow (Macrovoci)'].str.contains("SALDO|\\-", case=False, regex=True)]
            else:
                df_summary_show = df_summary
                
            # Visualizzazione pulita del solo schema senza totali calcolati in fondo alla tabella
            st.dataframe(df_summary_show, use_container_width=True, hide_index=True)

# --- IMPOSTAZIONI ---
elif menu == "IMPOSTAZIONI":
    st.subheader(t("config_app"))
    
    with st.expander(t("gest_cat")):
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.markdown(f"#### 📥 {t('entrata')}")
            new_cat_in = st.text_input("Nuova categoria entrata", key="input_new_cat_in")
            if st.button("Aggiungi Entrata", key="btn_add_cat_in"):
                if new_cat_in.strip() and new_cat_in not in st.session_state.cats_in:
                    st.session_state.cats_in.append(new_cat_in.strip())
                    st.success("✅ Aggiunta con successo!")
                    st.rerun()
                elif not new_cat_in.strip():
                    st.warning("Inserisci un nome valido.")
                else:
                    st.info("Esiste già.")
            
            st.markdown("##### Categorie attuali:")
            for cat in list(st.session_state.cats_in):
                c_del1, c_del2 = st.columns([3, 1])
                c_del1.text(cat)
                if c_del2.button("🗑️", key=f"del_cat_in_{cat}"):
                    if len(st.session_state.cats_in) > 1:
                        st.session_state.cats_in.remove(cat)
                        st.rerun()
                    else:
                        st.error("Minimo 1.")

        with col_c2:
            st.markdown(f"#### 📤 {t('uscita')}")
            new_cat_out = st.text_input("Nuova categoria uscita", key="input_new_cat_out")
            if st.button("Aggiungi Uscita", key="btn_add_cat_out"):
                if new_cat_out.strip() and new_cat_out not in st.session_state.cats_out:
                    st.session_state.cats_out.append(new_cat_out.strip())
                    st.success("✅ Aggiunta con successo!")
                    st.rerun()
                elif not new_cat_out.strip():
                    st.warning("Inserisci un nome valido.")
                else:
                    st.info("Esiste già.")
            
            st.markdown("##### Categorie attuali:")
            for cat in list(st.session_state.cats_out):
                c_del1, c_del2 = st.columns([3, 1])
                c_del1.text(cat)
                if c_del2.button("🗑️", key=f"del_cat_out_{cat}"):
                    if len(st.session_state.cats_out) > 1:
                        st.session_state.cats_out.remove(cat)
                        st.rerun()
                    else:
                        st.error("Minimo 1.")

    with st.expander(t("pref_ling")):
        selected_lang = st.selectbox(t("lingua"), LANGS, index=LANGS.index(st.session_state.settings['lang']))
        selected_curr = st.selectbox(t("valuta"), CURRS, index=CURRS.index(st.session_state.settings['currency']))
        
        if st.button(t("btn_salva_set"), key="btn_save_set"):
            st.session_state.settings['lang'] = selected_lang
            st.session_state.settings['currency'] = selected_curr
            st.success(t("succ_set"))
            st.rerun()
