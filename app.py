import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client

# Configurazione della pagina
st.set_page_config(page_title="MY FINANCE PRO", layout="wide")

# Connessione a Supabase tramite i Secrets di Streamlit Cloud
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Inizializzazione dello stato utente
if 'user' not in st.session_state:
    st.session_state.user = None

# --- FUNZIONE PRIVACY E TERMINI ---
def show_legal_texts():
    st.markdown("### 📜 Termini e Condizioni di Utilizzo")
    st.markdown("""
    1. **Natura del Servizio**: *MY FINANCE PRO* è un software di gestione finanziaria personale fornito "così com'è" (*as is*). Non costituisce consulenza finanziaria o fiscale.
    2. **Limitazione di Responsabilità**: L'autore declina ogni responsabilità per perdite economiche o errori di calcolo derivanti dall'uso dell'applicazione.
    3. **Accuratezza dei Dati**: L'utente è il solo responsabile della veridicità e della sicurezza delle credenziali e dei dati inseriti.
    """)
    st.markdown("### 🛡️ Informativa sulla Privacy (GDPR Compliance)")
    st.markdown("""
    1. **Titolare del Trattamento**: I dati sono trattati in conformità al GDPR.
    2. **Conservazione**: I dati di accesso e contabili sono salvati su un database remoto cifrato gestito tramite **Supabase**.
    3. **Diritti dell'Utente**: L'utente ha il diritto di accedere ai propri dati o di richiederne la cancellazione permanente.
    """)

# --- BARRA LATERALE ---
with st.sidebar:
    st.title("🧭 Navigazione")
    if st.button("ℹ️ Termini e Privacy"):
        st.session_state.show_legal = True
    
    if st.session_state.user:
        st.divider()
        if st.button("🚪 Logout"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()

# Gestione visualizzazione schermata legale
if getattr(st.session_state, 'show_legal', False):
    st.title("📄 Informazioni Legali")
    show_legal_texts()
    if st.button("⬅️ Torna all'app"):
        st.session_state.show_legal = False
        st.rerun()
    st.stop()

# --- AUTENTICAZIONE CON SUPABASE ---
if not st.session_state.user:
    st.title("🔐 Login / Registrazione")
    tab1, tab2 = st.tabs(["Accedi", "Registrati"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pwd")
        if st.button("Accedi"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.success("Accesso effettuato con successo!")
                st.rerun()
            except Exception as e:
                st.error("Credenziali errate o errore di accesso.")

    with tab2:
        email_r = st.text_input("Email", key="reg_email")
        password_r = st.text_input("Password", type="password", key="reg_pwd")
        accept = st.checkbox("Accetto i Termini di Servizio e la Privacy Policy")
        if st.button("Registrati"):
            if not accept:
                st.warning("Devi accettare i termini per registrarti.")
            else:
                try:
                    supabase.auth.sign_up({"email": email_r, "password": password_r})
                    st.success("Registrazione completata! Controlla la tua email per confermare l'account.")
                except Exception as e:
                    st.error(f"Errore durante la registrazione: {e}")
    st.stop()

# --- APPLICAZIONE PRINCIPALE (DASHBOARD) ---
st.title("⚡ MY FINANCE PRO")
st.write(f"Benvenuto nel tuo gestionale, **{st.session_state.user.email}**!")

# Sezioni principali della dashboard finanziaria
tab_dash, tab_trans, tab_report = st.tabs(["📊 Panoramica", "💰 Transazioni", "📈 Report e Grafici"])

with tab_dash:
    st.subheader("Riepilogo Finanziario")
    col1, col2, col3 = st.columns(3)
    col1.metric("Entrate Totali", "€ 0.00")
    col2.metric("Uscite Totali", "€ 0.00")
    col3.metric("Bilancio Attuale", "€ 0.00")

with tab_trans:
    st.subheader("Inserisci Nuova Transazione")
    with st.form("trans_form"):
        t_desc = st.text_input("Descrizione")
        t_amount = st.number_input("Importo (€)", value=0.0)
        t_type = st.selectbox("Tipo", ["Entrata", "Uscita"])
        submitted = st.form_submit_button("Salva Transazione")
        if submitted:
            st.success(f"Transazione registrata: {t_desc} - {t_amount} € ({t_type})")

with tab_report:
    st.subheader("Analisi delle Spese")
    df_dummy = pd.DataFrame({"Categoria": ["Casa", "Alimentari", "Svago", "Bollette"], "Valore": [450, 300, 150, 200]})
    fig = px.pie(df_dummy, names="Categoria", values="Valore", title="Distribuzione Spese per Categoria")
    st.plotly_chart(fig, use_container_width=True)
