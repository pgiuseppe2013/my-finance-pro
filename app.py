import streamlit as st
from supabase import create_client

# Configurazione Supabase
# Assicurati di impostare queste chiavi nei "Secrets" di Streamlit Cloud
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="MY FINANCE PRO", layout="wide")

# --- FUNZIONE PRIVACY E TERMINI ---
def show_legal_texts():
    st.markdown("### 📜 Termini e Condizioni")
    st.write("L'app è fornita 'così com'è'. L'utente è responsabile dei dati inseriti.")
    st.markdown("### 🛡️ Informativa Privacy (Supabase)")
    st.write("I dati sono salvati in modo cifrato su Supabase. Nessun dato è venduto a terzi.")

# --- BARRA LATERALE PER PRIVACY ---
with st.sidebar:
    st.title("Menu")
    if st.button("ℹ️ Termini e Privacy"):
        st.session_state.show_legal = True
    else:
        st.session_state.show_legal = False

# Gestione visualizzazione legale
if getattr(st.session_state, 'show_legal', False):
    show_legal_texts()
    st.stop()

# --- AUTENTICAZIONE CON SUPABASE ---
if not st.session_state.get('user'):
    st.title("🔐 Login / Registrazione")
    tab1, tab2 = st.tabs(["Accedi", "Registrati"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pwd")
        if st.button("Accedi"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.rerun()
            except Exception as e:
                st.error("Credenziali errate")

    with tab2:
        email_r = st.text_input("Email", key="reg_email")
        password_r = st.text_input("Password", type="password", key="reg_pwd")
        if st.button("Registrati"):
            try:
                supabase.auth.sign_up({"email": email_r, "password": password_r})
                st.success("Registrazione completata! Controlla la tua email.")
            except Exception as e:
                st.error(f"Errore: {e}")
    st.stop()

# --- APP PRINCIPALE ---
st.title("⚡ MY FINANCE PRO")
if st.button("Logout"):
    supabase.auth.sign_out()
    st.session_state.user = None
    st.rerun()
