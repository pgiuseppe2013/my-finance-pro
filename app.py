import streamlit as st
import pandas as pd
import datetime
from datetime import date
import plotly.express as px

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="MY FINANCE PRO", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #cbd5e1; }
    .stButton>button { border-radius: 8px; background: linear-gradient(145deg, #0f172a, #1e293b); color: #f8fafc; border: 1px solid #334155; padding: 8px 16px; font-weight: 600; }
    .stButton>button:hover { border-color: #22c55e; color: #22c55e; }
    div[data-testid="stMetricValue"] { color: #22c55e; font-family: 'Urbanist', sans-serif; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# 2. TESTI LEGALI (MODULARI E ESAUSTIVI)
def render_privacy_policy():
    st.markdown("""
    **INFORMATIVA PRIVACY (GDPR)**
    Il Titolare tratta i tuoi dati (Email, Username, dati finanziari inseriti) esclusivamente per fornire il servizio di gestione bilancio. I dati sono conservati localmente. Non cediamo dati a terzi. Hai diritto ad accesso, rettifica e cancellazione (Art. 15-22 GDPR).
    """)

def render_terms_conditions():
    st.markdown("""
    **TERMINI DI SERVIZIO**
    Software fornito "as-is". Lo sviluppatore non fornisce consulenza finanziaria; l'utente è unico responsabile delle decisioni prese basandosi sui dati elaborati dal software. La proprietà intellettuale è riservata. L'uso illecito comporterà l'immediata sospensione dell'account.
    """)

# 3. STATO SESSIONE
if 'users' not in st.session_state: st.session_state.users = []
if 'logged_user' not in st.session_state: st.session_state.logged_user = None
if 'accounts' not in st.session_state: st.session_state.accounts = []
if 'movements' not in st.session_state: st.session_state.movements = []
if 'settings' not in st.session_state: st.session_state.settings = {"lang": "IT", "currency": "EUR"}

# 4. GESTIONE ACCESSO / REGISTRAZIONE
if not st.session_state.logged_user:
    st.title("🔐 MY FINANCE PRO - Accesso")
    tab_login, tab_register = st.tabs(["Accedi", "Registrati"])
    
    with tab_login:
        l_user = st.text_input("Username o Email", key="log_user")
        l_pass = st.text_input("Password", type="password", key="log_pass")
        if st.button("Login"):
            user_found = next((u for u in st.session_state.users if u['user'] == l_user), None)
            if user_found:
                st.session_state.logged_user = l_user
                st.rerun()
            else: st.error("Credenziali non valide.")
                
    with tab_register:
        r_email = st.text_input("Email", key="reg_email")
        r_user = st.text_input("Username", key="reg_user")
        r_pass = st.text_input("Password", type="password", key="reg_pass")
        
        with st.expander("📖 Leggi Privacy Policy"): render_privacy_policy()
        with st.expander("📖 Leggi Termini e Condizioni"): render_terms_conditions()
        
        acc_privacy = st.checkbox("Accetto la Privacy Policy")
        acc_terms = st.checkbox("Accetto i Termini e Condizioni")
        
        if st.button("Registrati"):
            if not r_email or not r_user or not r_pass: st.error("Compila tutti i campi.")
            elif not acc_privacy or not acc_terms: st.error("Devi accettare termini e privacy.")
            else:
                st.session_state.users.append({"email": r_email, "user": r_user, "pass": r_pass})
                st.success("Registrato! Ora puoi fare il login.")
    st.stop()

# 5. APP CORE (DOPO IL LOGIN)
st.sidebar.title(f"Benvenuto, {st.session_state.logged_user}")
menu = st.sidebar.radio("Navigazione", ["DASHBOARD", "MOVIMENTI", "IMPOSTAZIONI"])

if st.sidebar.button("Logout"):
    st.session_state.logged_user = None
    st.rerun()

if menu == "DASHBOARD":
    st.header("📊 Dashboard")
    # Qui inserisci i grafici e le metriche che avevamo previsto
    st.metric("Saldo Totale", "€ 0,00")

elif menu == "MOVIMENTI":
    st.header("💳 Movimenti")
    # Logica di inserimento movimenti
    col1, col2 = st.columns(2)
    with col1:
        desc = st.text_input("Descrizione")
        imp = st.number_input("Importo", step=0.01)
    with col2:
        tipo = st.selectbox("Tipo", ["Entrata", "Uscita"])
        data = st.date_input("Data")
    if st.button("Salva Movimento"):
        st.session_state.movements.append({"desc": desc, "imp": imp, "tipo": tipo, "data": data})
        st.success("Salvato!")

elif menu == "IMPOSTAZIONI":
    st.header("⚙️ Impostazioni")
    with st.expander("⚖️ Note Legali"):
        render_privacy_policy()
        render_terms_conditions()
    
    # Impostazioni lingua/valuta
    lang = st.selectbox("Lingua", ["Italiano", "Inglese"])
    if st.button("Salva Preferenze"):
        st.session_state.settings["lang"] = lang
        st.success("Salvato.")
