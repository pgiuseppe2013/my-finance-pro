import streamlit as st
import pandas as pd
import datetime
from datetime import date, timedelta
import plotly.express as px

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="MY FINANCE PRO", page_icon="⚡", layout="wide")

# 2. INIZIALIZZAZIONE STATO (Eseguita subito dopo le importazioni)
def init_state():
    defaults = {
        'users': [], 'logged_user': None, 'accounts': [], 'movements': [],
        'settings': {"lang": "IT", "currency": "EUR"},
        'active_tab': "DASHBOARD"
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# 3. FUNZIONI DI SUPPORTO
def show_legal_texts():
    st.markdown("### 📜 Termini e Condizioni")
    st.write("1. **Utilizzo**: L'applicazione è fornita a scopo dimostrativo.")
    st.write("2. **Responsabilità**: L'utente è responsabile dei dati inseriti.")
    st.markdown("### 🛡️ Informativa sulla Privacy")
    st.write("- **Memorizzazione**: I dati risiedono solo nella sessione temporanea del browser.")
    st.write("- **Nessun Tracciamento**: Non vengono inviati dati a server esterni.")

# 4. LOGICA DI AUTENTICAZIONE
if not st.session_state.logged_user:
    st.title("🔐 Login / Registrazione")
    
    with st.expander("📄 Termini e Privacy"):
        show_legal_texts()
        
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Accedi")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Accedi"):
            user = next((x for x in st.session_state.users if x['u'] == u and x['p'] == p), None)
            if user:
                st.session_state.logged_user = u
                st.rerun()
            else:
                st.error("Credenziali errate")
    with col2:
        st.subheader("Registrati")
        u_reg = st.text_input("Nuovo Username")
        p_reg = st.text_input("Nuova Password", type="password")
        accept = st.checkbox("Accetto i Termini e la Privacy Policy")
        if st.button("Registrati"):
            if accept:
                st.session_state.users.append({'u': u_reg, 'p': p_reg})
                st.success("Registrato con successo!")
            else:
                st.warning("Devi accettare i termini per registrarti.")
    st.stop()

# 5. INTERFACCIA PRINCIPALE (Se loggato)
st.title("⚡ MY FINANCE PRO")

# Menu di navigazione
menu = st.columns(4)
if menu[0].button("📊 DASHBOARD"): st.session_state.active_tab = "DASHBOARD"
if menu[1].button("📝 MOVIMENTI"): st.session_state.active_tab = "MOVIMENTI"
if menu[2].button("📈 REPORT"): st.session_state.active_tab = "REPORT"
if menu[3].button("⚙️ IMPOSTAZIONI"): st.session_state.active_tab = "IMPOSTAZIONI"

# Logica delle sezioni
if st.session_state.active_tab == "DASHBOARD":
    st.subheader("Dashboard")
    st.metric("LIQUIDITÀ TOTALE", "0.00 EUR")
    if st.expander("➕ Aggiungi Conto"):
        st.text_input("Nome Conto")
        st.button("Salva Conto")

elif st.session_state.active_tab == "MOVIMENTI":
    st.subheader("Registra Operazione")
    st.date_input("Data")
    st.number_input("Importo", step=0.01)
    st.button("Registra")

elif st.session_state.active_tab == "IMPOSTAZIONI":
    st.subheader("Impostazioni")
    with st.expander("ℹ️ Informazioni Legali e Privacy"):
        show_legal_texts()
    if st.button("Logout"):
        st.session_state.logged_user = None
        st.rerun()

elif st.session_state.active_tab == "REPORT":
    st.subheader("Report")
    st.info("Nessun dato disponibile.")
