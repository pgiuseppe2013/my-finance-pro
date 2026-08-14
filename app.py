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

# 2. INIZIALIZZAZIONE STATO & AUTENTICAZIONE UTENTI
if 'users' not in st.session_state:
    st.session_state.users = []
if 'logged_user' not in st.session_state:
    st.session_state.logged_user = None
# ... (altri stati rimangono invariati)
if 'accounts' not in st.session_state: st.session_state.accounts = []
if 'movements' not in st.session_state: st.session_state.movements = []
if 'settings' not in st.session_state: st.session_state.settings = {"lang": "IT", "currency": "EUR"}
if 'active_tab' not in st.session_state: st.session_state.active_tab = "DASHBOARD"
if 'cats_in' not in st.session_state: st.session_state.cats_in = ["Stipendio", "Rendita", "Bonus", "Vendita", "Altro"]
if 'cats_out' not in st.session_state: st.session_state.cats_out = ["Affitto", "Mutuo", "Utenze", "Supermercato", "Shopping", "Trasporti", "Salute", "Svago"]

### [MODIFICA PRIVACY/CONDIZIONI] Funzioni per documenti
def show_legal_texts():
    st.markdown("### 📜 Termini, Condizioni e Privacy")
    with st.expander("Privacy Policy"):
        st.write("I tuoi dati finanziari vengono salvati esclusivamente in locale nella memoria temporanea del browser. Nessun dato viene trasmesso a server esterni.")
    with st.expander("Termini e Condizioni di Utilizzo"):
        st.write("L'utilizzo del software è fornito 'così com'è'. L'utente è l'unico responsabile dei dati inseriti.")

# --- GESTIONE SCHERMATA DI ACCESSO / REGISTRAZIONE ---
if not st.session_state.logged_user:
    st.title("🔐 Accesso a MY FINANCE PRO")
    tab_login, tab_register = st.tabs(["Accedi", "Crea un nuovo account"])
    
    with tab_login:
        l_user = st.text_input("Username", key="login_user")
        l_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", key="btn_login_action"):
            user_found = next((u for u in st.session_state.users if u['username'] == l_user and u['password'] == l_pass), None)
            if user_found:
                st.session_state.logged_user = l_user
                st.success("Accesso effettuato!")
                st.rerun()
            else:
                st.error("Credenziali non valide.")
                
    with tab_register:
        r_user = st.text_input("Scegli uno Username", key="reg_user")
        r_pass = st.text_input("Scegli una Password", type="password", key="reg_pass")
        ### [MODIFICA PRIVACY/CONDIZIONI] Checkbox obbligatoria in registrazione
        accettazione = st.checkbox("Accetto la Privacy Policy e i Termini di Utilizzo")
        show_legal_texts()
        
        if st.button("Registrati", key="btn_register_action"):
            if not r_user.strip() or not r_pass.strip():
                st.warning("Inserisci credenziali.")
            elif not accettazione:
                st.error("Devi accettare termini e condizioni per procedere.")
            elif any(u['username'] == r_user for u in st.session_state.users):
                st.error("Username occupato.")
            else:
                st.session_state.users.append({"username": r_user, "password": r_pass, "accepted_legal": True})
                st.success("Account creato! Ora effettua il login.")
    st.stop()

# ... (IL RESTO DEL CODICE RESTA INVARIATO FINO ALLE IMPOSTAZIONI) ...

# --- IMPOSTAZIONI ---
elif menu == "IMPOSTAZIONI":
    st.subheader(t("config_app"))
    
    ### [MODIFICA PRIVACY/CONDIZIONI] Sezione dedicata nei settings
    with st.expander("⚖️ Note Legali"):
        show_legal_texts()
        st.info("Hai accettato i termini il giorno della registrazione.")

    with st.expander(t("gest_cat")):
        # ... (il codice esistente delle categorie rimane qui)
        pass 

    with st.expander(t("pref_ling")):
        # ... (il codice esistente di lingua e valuta rimane qui)
        selected_lang = st.selectbox(t("lingua"), LANGS, index=LANGS.index(st.session_state.settings['lang']))
        selected_curr = st.selectbox(t("valuta"), CURRS, index=CURRS.index(st.session_state.settings['currency']))
        
        if st.button(t("btn_salva_set"), key="btn_save_set"):
            st.session_state.settings['lang'] = selected_lang
            st.session_state.settings['currency'] = selected_curr
            st.success(t("succ_set"))
            st.rerun()
