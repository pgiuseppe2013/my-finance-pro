import streamlit as st
import pandas as pd
import datetime
from datetime import date, timedelta
import plotly.express as px

# --- FUNZIONE TESTI LEGALI ---
def show_legal_texts():
    st.markdown("### 📜 Termini e Condizioni")
    st.write("""
    1. **Accettazione**: Utilizzando MY FINANCE PRO, l'utente accetta i presenti termini.
    2. **Responsabilità**: L'applicazione è fornita a scopo illustrativo. L'autore non si assume responsabilità per decisioni finanziarie basate sui dati inseriti.
    3. **Natura del servizio**: Questo è un software basato su sessioni locali.
    """)
    st.markdown("### 🛡️ Informativa sulla Privacy")
    st.write("""
    - **Raccolta Dati**: Non vengono raccolti dati su server esterni. Tutti i dati finanziari inseriti risiedono esclusivamente nella memoria temporanea del browser (session state).
    - **Sicurezza**: I dati vengono eliminati automaticamente al termine della sessione o alla chiusura del browser.
    - **Nessuna Terza Parte**: Nessuna informazione viene condivisa, venduta o processata da servizi terzi.
    """)

# ... (MANTENERE IL RESTO DEL TUO CODICE DI CONFIGURAZIONE E INIT_STATE) ...

# --- MODIFICA NELLA LOGICA DI LOGIN ---
if not st.session_state.logged_user:
    st.title("🔐 Login / Registrazione")
    
    with st.expander("📄 Consulta Termini e Privacy prima di registrarti"):
        show_legal_texts()
        
    # ... (Il tuo codice di login/registrazione) ...
    # Assicurati di aggiungere il checkbox:
    accept_tc = st.checkbox("Dichiaro di aver letto e accettato i Termini e la Privacy Policy")
    if st.button("Registrati"):
        if not accept_tc:
            st.error("Devi accettare i termini per proseguire.")
        else:
            # Procedi con la registrazione...
            pass

# --- MODIFICA NELLA LOGICA DI IMPOSTAZIONI ---
elif st.session_state.active_tab == "IMPOSTAZIONI":
    st.subheader(t("set"))
    # ... (il resto del codice impostazioni) ...
    
    with st.expander("ℹ️ Informazioni Legali e Privacy"):
        show_legal_texts()
        
    if st.button("Logout"):
        st.session_state.logged_user = None
        st.rerun()
