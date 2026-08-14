import streamlit as st
import pandas as pd
import datetime
from datetime import date
import plotly.express as px

# --- 1. CONFIGURAZIONE PAGINA E STILE ---
st.set_page_config(page_title="MY FINANCE PRO", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #cbd5e1; }
    .stButton>button { border-radius: 8px; background: linear-gradient(145deg, #0f172a, #1e293b); color: #f8fafc; border: 1px solid #334155; padding: 8px 16px; font-weight: 600; }
    .stButton>button:hover { border-color: #22c55e; color: #22c55e; }
    div[data-testid="stMetricValue"] { color: #22c55e; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FUNZIONI TESTI LEGALI ESAUSTIVI ---
def render_privacy_policy():
    st.markdown("""
    ### 🛡️ PRIVACY POLICY (GDPR 2016/679)
    **1. Titolare:** Gestore di MY FINANCE PRO.
    **2. Dati Raccolti:** Email, Username e dati finanziari inseriti.
    **3. Finalità:** Erogazione del servizio di gestione bilancio.
    **4. Conservazione:** I dati sono memorizzati in locale. Non cediamo informazioni a terzi.
    **5. Diritti:** Hai diritto di accesso, rettifica e cancellazione (Art. 15-22 GDPR).
    """)

def render_terms_conditions():
    st.markdown("""
    ### 📜 TERMINI E CONDIZIONI
    **1. Servizio:** Software "AS-IS". Non forniamo consulenza finanziaria.
    **2. Responsabilità:** L'utente è l'unico responsabile dei dati inseriti e delle decisioni economiche intraprese.
    **3. Proprietà:** Il codice e il design sono proprietà del creatore.
    **4. Sospensione:** Ci riserviamo il diritto di sospendere il servizio per manutenzione o violazioni.
    """)

# --- 3. INIZIALIZZAZIONE STATO ---
if 'users' not in st.session_state: st.session_state.users = []
if 'logged_user' not in st.session_state: st.session_state.logged_user = None
if 'movements' not in st.session_state: st.session_state.movements = []
if 'settings' not in st.session_state: st.session_state.settings = {"lang": "IT", "currency": "EUR"}

# --- 4. GESTIONE ACCESSO E REGISTRAZIONE ---
if not st.session_state.logged_user:
    st.title("🔐 MY FINANCE PRO - Accesso")
    tab_login, tab_register = st.tabs(["Accedi", "Registrati"])
    
    with tab_login:
        l_user = st.text_input("Username o Email", key="log_user")
        l_pass = st.text_input("Password", type="password", key="log_pass")
        if st.button("Accedi"):
            user_found = next((u for u in st.session_state.users if u['user'] == l_user), None)
            if user_found:
                st.session_state.logged_user = l_user
                st.rerun()
            else: st.error("Credenziali non valide.")
                
    with tab_register:
        r_email = st.text_input("Email")
        r_user = st.text_input("Scegli uno Username")
        r_pass = st.text_input("Scegli una Password", type="password")
        
        st.markdown("---")
        with st.expander("📖 Leggi la Privacy Policy completa"): render_privacy_policy()
        with st.expander("📖 Leggi i Termini e Condizioni completi"): render_terms_conditions()
        
        acc_privacy = st.checkbox("Accetto la Privacy Policy")
        acc_terms = st.checkbox("Accetto i Termini e Condizioni")
        
        if st.button("Registrati"):
            if not r_email or not r_user or not r_pass: st.error("Compila tutti i campi.")
            elif not acc_privacy or not acc_terms: st.error("Devi accettare Privacy e Termini.")
            else:
                st.session_state.users.append({"email": r_email, "user": r_user})
                st.success("Account creato! Ora effettua il login.")
    st.stop()

# --- 5. CORE DELL'APP (DOPO IL LOGIN) ---
st.sidebar.title(f"Bentornato {st.session_state.logged_user}")
menu = st.sidebar.radio("Navigazione", ["DASHBOARD", "MOVIMENTI", "IMPOSTAZIONI"])

if st.sidebar.button("Logout"):
    st.session_state.logged_user = None
    st.rerun()

if menu == "DASHBOARD":
    st.header("📊 Dashboard Finanziaria")
    st.metric("Saldo Totale", "€ 0,00")
    if st.session_state.movements:
        df = pd.DataFrame(st.session_state.movements)
        st.bar_chart(df.set_index("data")["imp"])

elif menu == "MOVIMENTI":
    st.header("💳 Gestione Movimenti")
    col1, col2 = st.columns(2)
    with col1:
        desc = st.text_input("Descrizione")
        imp = st.number_input("Importo", step=0.01)
    with col2:
        tipo = st.selectbox("Tipo", ["Entrata", "Uscita"])
        data = st.date_input("Data")
    
    if st.button("Salva Movimento"):
        st.session_state.movements.append({"desc": desc, "imp": imp, "tipo": tipo, "data": data})
        st.success("Movimento salvato!")

elif menu == "IMPOSTAZIONI":
    st.header("⚙️ Impostazioni")
    with st.expander("⚖️ Documentazione Legale"):
        render_privacy_policy()
        render_terms_conditions()
    
    lang = st.selectbox("Lingua", ["Italiano", "Inglese"])
    if st.button("Salva Preferenze"):
        st.session_state.settings["lang"] = lang
        st.success("Preferenze aggiornate.")
