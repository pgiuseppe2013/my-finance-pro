import streamlit as st
import datetime

# --- CONFIGURAZIONE E STILE ---
st.set_page_config(page_title="MY FINANCE PRO", page_icon="⚡", layout="wide")

# --- INIZIALIZZAZIONE STATO ---
if 'users' not in st.session_state: st.session_state.users = []
if 'logged_user' not in st.session_state: st.session_state.logged_user = None

# --- FUNZIONI TESTI LEGALI (ESPANDIBILI) ---
def privacy_text():
    st.markdown("""
    **Privacy Policy:** Il trattamento dei dati avviene nel rispetto del GDPR. I dati sono conservati localmente. Non condividiamo informazioni con terze parti.
    """)

def terms_text():
    st.markdown("""
    **Termini di Servizio:** Il servizio è fornito "così com'è". L'utente è responsabile dell'uso del software e della custodia delle proprie credenziali.
    """)

# --- SCHERMATA LOGIN / REGISTRAZIONE ---
if not st.session_state.logged_user:
    st.title("🔐 MY FINANCE PRO - Accesso")
    tab_login, tab_register = st.tabs(["Accedi", "Registrati"])
    
    with tab_login:
        l_user = st.text_input("Username o Email", key="log_user")
        l_pass = st.text_input("Password", type="password", key="log_pass")
        if st.button("Accedi"):
            # Logica di verifica (esempio)
            st.session_state.logged_user = l_user
            st.rerun()
                
    with tab_register:
        st.subheader("Crea il tuo Account")
        r_email = st.text_input("Inserisci la tua Email")
        r_user = st.text_input("Scegli uno Username")
        r_pass = st.text_input("Scegli una Password", type="password")
        
        st.markdown("---")
        
        # Expanders per la lettura volontaria
        with st.expander("📖 Leggi la Privacy Policy"):
            privacy_text()
        with st.expander("📖 Leggi i Termini e Condizioni"):
            terms_text()
            
        # Flag obbligatori
        accetto_privacy = st.checkbox("Accetto la Privacy Policy")
        accetto_termini = st.checkbox("Accetto i Termini e Condizioni")
        
        if st.button("Registrati"):
            if not r_email or not r_user or not r_pass:
                st.error("Tutti i campi sono obbligatori.")
            elif not accetto_privacy or not accetto_termini:
                st.error("Devi accettare Privacy e Termini per procedere.")
            else:
                # Salva utente (esempio)
                st.session_state.users.append({"email": r_email, "username": r_user})
                st.success("Registrazione completata! Ora puoi effettuare il login.")

    st.stop()

# --- AREA RISERVATA ---
st.sidebar.title(f"Bentornato {st.session_state.logged_user}")
if st.sidebar.button("Logout"):
    st.session_state.logged_user = None
    st.rerun()

st.title("Dashboard")
st.write("Area privata attiva.")
