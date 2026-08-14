import streamlit as st
import pandas as pd
import datetime
from datetime import date, timedelta
import plotly.express as px

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="MY FINANCE PRO", page_icon="⚡", layout="wide")

# 2. INIZIALIZZAZIONE STATO
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

# 3. TESTI LEGALI DETTAGLIATI E PROFESSIONALI
def show_legal_texts():
    st.markdown("### 📜 Termini e Condizioni di Utilizzo")
    st.markdown("""
    1. **Natura del Servizio**: *MY FINANCE PRO* è un software di gestione finanziaria personale fornito "così com'è" (*as is*), a solo scopo dimostrativo, informativo ed educativo. Non costituisce in alcun modo una consulenza finanziaria, fiscale o di investimento professionale.
    2. **Limitazione di Responsabilità**: L'autore e gli sviluppatori declinano ogni responsabilità per eventuali perdite economiche, errori di calcolo, omissioni o danni derivanti dall'uso diretto o indiretto dell'applicazione e delle informazioni in essa inserite.
    3. **Accuratezza dei Dati**: L'utente è l'unico ed esclusivo responsabile dell'accuratezza, della sicurezza e della veridicità dei dati contabili e finanziari inseriti all'interno della piattaforma.
    4. **Modifiche al Servizio**: L'autore si riserva il diritto di modificare, sospendere o interrompere, temporaneamente o permanentemente, l'applicazione in qualsiasi momento e senza preavviso.
    """)
    
    st.markdown("### 🛡️ Informativa sulla Privacy (GDPR Compliance Preview)")
    st.markdown("""
    1. **Titolare del Trattamento**: I dati sono gestiti nell'ambito dell'utilizzo del software.
    2. **Tipologia di Dati Raccolti**: 
       * Dati di autenticazione (Username e credenziali d'accesso).
       * Dati finanziari inseriti volontariamente (conti, importi, categorie, movimenti).
    3. **Modalità e Luogo di Conservazione**: 
       * I dati possono essere elaborati nella memoria di sessione temporanea del browser oppure memorizzati su infrastrutture di database sécurisées (es. servizi cloud come Supabase o analoghi, se configurati). 
    4. **Finalità del Trattamento**: I dati inseriti vengono trattati esclusivamente al fine di erogare le funzionalità core dell'applicazione di bilancio personale. Nessun dato finanziario viene ceduto, venduto o condiviso con terze parti per scopi commerciali o di profilazione.
    5. **Diritti dell'Utente**: L'utente può richiedere in qualsiasi momento la cancellazione del proprio account e dei dati associati azzerando le informazioni salvate.
    """)

# 4. LOGICA DI AUTENTICAZIONE
if not st.session_state.logged_user:
    st.title("🔐 Login / Registrazione")
    
    with st.expander("📄 Leggi Termini, Condizioni e Privacy Policy prima di procedere"):
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
        accept = st.checkbox("Dichiaro di aver letto, compreso e di accettare integralmente i Termini di Servizio e l'Informativa sulla Privacy.")
        if st.button("Registrati"):
            if accept:
                st.session_state.users.append({'u': u_reg, 'p': p_reg})
                st.success("Registrato con successo! Effettua il login a sinistra.")
            else:
                st.warning("Devi obbligatoriamente accettare i Termini e la Privacy Policy per registrarti.")
    st.stop()

# 5. INTERFACCIA PRINCIPALE
st.title("⚡ MY FINANCE PRO")

menu = st.columns(4)
if menu[0].button("📊 DASHBOARD"): st.session_state.active_tab = "DASHBOARD"
if menu[1].button("📝 MOVIMENTI"): st.session_state.active_tab = "MOVIMENTI"
if menu[2].button("📈 REPORT"): st.session_state.active_tab = "REPORT"
if menu[3].button("⚙️ IMPOSTAZIONI"): st.session_state.active_tab = "IMPOSTAZIONI"

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
    with st.expander("ℹ️ Informazioni Legali, Termini e Privacy Policy"):
        show_legal_texts()
    if st.button("Logout"):
        st.session_state.logged_user = None
        st.rerun()

elif st.session_state.active_tab == "REPORT":
    st.subheader("Report")
    st.info("Nessun dato disponibile.")
