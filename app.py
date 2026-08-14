import streamlit as st
import pandas as pd
import datetime
from datetime import date, timedelta
import plotly.express as px

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="MY FINANCE PRO", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #cbd5e1; }
    .stButton>button { border-radius: 8px; font-weight: 600; }
    div[data-testid="stMetricValue"] { color: #22c55e; }
    </style>
    """, unsafe_allow_html=True)

# 2. INIZIALIZZAZIONE STATO
def init_state():
    defaults = {
        'users': [], 'logged_user': None, 'accounts': [], 'movements': [],
        'settings': {"lang": "IT", "currency": "EUR"},
        'active_tab': "DASHBOARD",
        'cats_in': ["Stipendio", "Rendita", "Bonus", "Vendita", "Altro"],
        'cats_out': ["Affitto", "Mutuo", "Utenze", "Supermercato", "Shopping", "Trasporti", "Svago"]
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# 3. TRADUZIONI & UTILITY
TRANSLATIONS = {
    "IT": {"title": "⚡ MY FINANCE PRO", "dash": "📊 DASHBOARD", "mov": "📝 MOVIMENTI", "rep": "📈 REPORT", "set": "⚙️ IMPOSTAZIONI", "tot_liq": "LIQUIDITÀ TOTALE"},
    "EN": {"title": "⚡ MY FINANCE PRO", "dash": "📊 DASHBOARD", "mov": "📝 TRANSACTIONS", "rep": "📈 REPORT", "set": "⚙️ SETTINGS", "tot_liq": "TOTAL LIQUIDITY"}
}

def t(key):
    lang = st.session_state.settings["lang"]
    return TRANSLATIONS.get(lang, TRANSLATIONS["EN"]).get(key, key)

# --- AUTENTICAZIONE & PRIVACY ---
if not st.session_state.logged_user:
    st.title("🔐 Login / Registrazione")
    
    # Sezione Informativa Privacy e T&C visibile in fase di accesso
    with st.expander("📄 Termini e Condizioni & Informativa sulla Privacy"):
        st.markdown("""
        **Informativa sulla Privacy e Termini di Servizio:**
        * I dati inseriti sono gestiti nel rispetto della privacy e memorizzati temporaneamente nella sessione.
        * Nessun dato finanziario personale viene condiviso con terze parti o memorizzato su database esterni persistenti in questa versione demo.
        * Utilizzando l'applicazione, accetti i termini di utilizzo di base per la gestione amatoriale della finanza personale.
        """)
        
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Accedi")
        u_log = st.text_input("Username", key="log_u")
        p_log = st.text_input("Password", type="password", key="log_p")
        if st.button("Accedi"):
            user = next((x for x in st.session_state.users if x['u'] == u_log and x['p'] == p_log), None)
            if user: 
                st.session_state.logged_user = u_log
                st.rerun()
            else: 
                st.error("Credenziali errate")
                
    with col2:
        st.subheader("Registrati")
        u_reg = st.text_input("Username", key="reg_u")
        p_reg = st.text_input("Password", type="password", key="reg_p")
        accept_tc = st.checkbox("Accetto i Termini e Condizioni e la Privacy Policy")
        
        if st.button("Registrati"):
            if not accept_tc:
                st.error("Devi accettare i Termini e Condizioni per registrarti.")
            elif not u_reg or not p_reg:
                st.error("Inserisci username e password validi.")
            else:
                st.session_state.users.append({'u': u_reg, 'p': p_reg})
                st.success("Registrazione completata! Ora puoi effettuare il login a sinistra.")
    st.stop()

# --- LOGICA APPLICATIVA ---
def get_user_data():
    return [a for a in st.session_state.accounts if a['user'] == st.session_state.logged_user], \
           [m for m in st.session_state.movements if m['user'] == st.session_state.logged_user]

user_accounts, user_movements = get_user_data()

# 4. DASHBOARD & INTERFACCIA
st.title(t("title"))
tab1, tab2, tab3, tab4 = st.columns(4)
if tab1.button(t("dash")): st.session_state.active_tab = "DASHBOARD"
if tab2.button(t("mov")): st.session_state.active_tab = "MOVIMENTI"
if tab3.button(t("rep")): st.session_state.active_tab = "REPORT"
if tab4.button(t("set")): st.session_state.active_tab = "IMPOSTAZIONI"

# --- LOGICA VIEW ---
if st.session_state.active_tab == "DASHBOARD":
    st.subheader("Panoramica Patrimoniale")
    total_bal = sum(a['init_bal'] for a in user_accounts if a['type'] != "Carta di Credito")
    total_bal += sum(m['amt'] for m in user_movements if not m.get('virtual'))
    st.metric(t("tot_liq"), f"{total_bal:,.2f} {st.session_state.settings['currency']}")
    
    with st.expander("➕ Aggiungi Conto"):
        name = st.text_input("Nome Conto")
        tipo = st.selectbox("Tipo", ["Bancario", "Prepagata", "Carta di Credito"])
        if st.button("Salva Conto"):
            st.session_state.accounts.append({
                'user': st.session_state.logged_user, 
                'id': len(st.session_state.accounts), 
                'name': name, 
                'type': tipo, 
                'init_bal': 0.0
            })
            st.rerun()

elif st.session_state.active_tab == "MOVIMENTI":
    st.subheader("Registra Operazione")
    if not user_accounts:
        st.warning("Crea prima almeno un conto nella Dashboard.")
    else:
        col1, col2, col3 = st.columns(3)
        date_c = col1.date_input("Data")
        acc = col2.selectbox("Conto", [a['name'] for a in user_accounts])
        amt = col3.number_input("Importo", step=0.01)
        if st.button("Registra"):
            st.session_state.movements.append({
                'user': st.session_state.logged_user, 
                'date_c': date_c, 
                'acc': acc, 
                'amt': amt, 
                'virtual': False
            })
            st.rerun()

    if user_movements:
        df = pd.DataFrame(user_movements)
        st.dataframe(df, use_container_width=True)

elif st.session_state.active_tab == "REPORT":
    if user_movements:
        df = pd.DataFrame(user_movements)
        df['date_c'] = pd.to_datetime(df['date_c'])
        fig = px.bar(df, x='date_c', y='amt', color='acc', title="Analisi Flussi")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nessun dato per il report.")

elif st.session_state.active_tab == "IMPOSTAZIONI":
    st.subheader(t("set"))
    st.session_state.settings['lang'] = st.selectbox(
        "Lingua", ["IT", "EN"], 
        index=["IT", "EN"].index(st.session_state.settings['lang'])
    )
    
    with st.expander("📄 Termini e Condizioni & Privacy Policy"):
        st.markdown("""
        **Informativa sulla Privacy (Dettagli):**
        I dati trattati risiedono unicamente nella sessione corrente dell'applicazione. Puoi consultare in qualsiasi momento le specifiche di utilizzo.
        """)
        
    if st.button("Logout"):
        st.session_state.logged_user = None
        st.rerun()
