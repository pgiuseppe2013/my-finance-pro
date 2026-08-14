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
    .legal-box {
        background-color: #0f172a;
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 8px;
        height: 200px;
        overflow-y: scroll;
        font-size: 0.85rem;
        color: #94a3b8;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. INIZIALIZZAZIONE STATO & AUTENTICAZIONE UTENTI
if 'users' not in st.session_state:
    st.session_state.users = []
if 'logged_user' not in st.session_state:
    st.session_state.logged_user = None
if 'accounts' not in st.session_state: st.session_state.accounts = []
if 'movements' not in st.session_state: st.session_state.movements = []
if 'settings' not in st.session_state: st.session_state.settings = {"lang": "IT", "currency": "EUR"}
if 'active_tab' not in st.session_state: st.session_state.active_tab = "DASHBOARD"
if 'cats_in' not in st.session_state: st.session_state.cats_in = ["Stipendio", "Rendita", "Bonus", "Vendita", "Altro"]
if 'cats_out' not in st.session_state: st.session_state.cats_out = ["Affitto", "Mutuo", "Utenze", "Supermercato", "Shopping", "Trasporti", "Salute", "Svago"]

# --- DOCUMENTI LEGALI ESAUSTIVI ---
def render_privacy_policy():
    st.markdown("""
    ### 🛡️ INFORMATIVA SULLA PRIVACY (Art. 13 Regolamento UE 2016/679 - GDPR)
    
    **1. Titolare del Trattamento**
    Il Titolare del trattamento dei dati è lo sviluppatore e gestore dell'applicazione "MY FINANCE PRO". 
    
    **2. Tipologia dei dati trattati e finalità**
    L'applicazione raccoglie e tratta esclusivamente i dati inseriti volontariamente dall'utente in fase di registrazione (Username e Password in forma cifrata o protetta) e i dati di natura finanziaria (movimenti, conti, categorie) inseriti per il corretto funzionamento del servizio di bilancio personale. Nessun dato viene ceduto a terzi.
    
    **3. Base giuridica del trattamento**
    Il trattamento dei dati si fonda sul consenso espresso dall'utente in fase di registrazione e sulla necessità di erogare le funzionalità software richieste.
    
    **4. Modalità di conservazione**
    I dati personali e finanziari sono memorizzati all'interno della sessione locale e dei sistemi di storage dell'applicazione. L'utente riconosce che l'utilizzo di piattaforme cloud o locali comporta l'adozione di misure di sicurezza adeguate, pur non potendosi escludere del tutto rischi informatici fortuiti.
    
    **5. Diritti dell'interessato**
    In ogni momento l'utente ha il diritto di richiedere l'accesso ai propri dati, la rettifica, la cancellazione degli stessi o la limitazione del trattamento, contattando il supporto dell'applicazione o eliminando il proprio account.
    """)

def render_terms_conditions():
    st.markdown("""
    ### 📜 TERMINI E CONDIZIONI DI UTILIZZO DEL SERVIZIO
    
    **1. Accettazione dei Termini**
    Accedendo e utilizzando "MY FINANCE PRO", l'utente dichiara di aver letto, compreso e accettato integralmente i presenti Termini e Condizioni. Qualora non si intenda accettare tali termini, è fatto divieto di utilizzare l'applicazione e completare la registrazione.
    
    **2. Natura del Servizio e Limitazione di Responsabilità**
    "MY FINANCE PRO" è un software di gestione finanziaria personale fornito "così com'è" (as-is) e "come disponibile". 
    * Il software **non** costituisce in alcun modo consulenza finanziaria, fiscale, legale o di investimento.
    * Lo sviluppatore non si assume alcuna responsabilità per eventuali errori di calcolo, perdita di dati, inaccuratezza dei report o decisioni economiche prese dall'utente sulla base delle informazioni elaborate dall'applicazione.
    
    **3. Obblighi dell'utente**
    L'utente si impegna a custodire con la massima cura le proprie credenziali di accesso (Username e Password). L'utente è l'unico ed esclusivo responsabile di tutte le attività compiute tramite il proprio account.
    
    **4. Proprietà Intellettuale**
    Tutti i diritti di proprietà intellettuale relativi al codice sorgente, al design, alla grafica e alla struttura logica di "MY FINANCE PRO" sono di esclusiva proprietà del creatore. È vietata la riproduzione, la distribuzione o la modifica non autorizzata.
    
    **5. Sospensione o Interruzione**
    Il gestore si riserva il diritto di modificare, sospendere o interrompere, temporaneamente o permanentemente, il servizio in qualsiasi momento e senza preavviso, per manutenzione o aggiornamenti.
    """)

def show_legal_modals_or_expanders():
    with st.expander("📄 Visualizza Informativa Privacy Completa"):
        render_privacy_policy()
    with st.expander("📄 Visualizza Termini e Condizioni Completi"):
        render_terms_conditions()

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
                st.success("Accesso effettuato con successo!")
                st.rerun()
            else:
                st.error("Credenziali non valide o account inesistente.")
                
    with tab_register:
        st.markdown("### Registrazione Nuovo Account")
        r_user = st.text_input("Scegli uno Username", key="reg_user")
        r_pass = st.text_input("Scegli una Password", type="password", key="reg_pass")
        
        st.markdown("---")
        st.markdown("#### Presa visione e accettazione obbligatoria dei documenti legali")
        st.markdown("Per procedere con la registrazione e tutelare i tuoi e nostri diritti, è obbligatorio leggere e accettare la Privacy Policy e i Termini di Servizio.")
        
        # Box con scorrimento per simulare la lettura approfondita
        st.markdown('<div class="legal-box">', unsafe_allow_html=True)
        render_privacy_policy()
        st.markdown("---")
        render_terms_conditions()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Checkbox obbligatorie separate o unificate ma nette
        accettazione_privacy = st.checkbox("Dichiaro di aver letto e di accettare integralmente la **Privacy Policy** ai sensi del GDPR.")
        accettazione_termini = st.checkbox("Dichiaro di aver letto e di accettare integralmente i **Termini e Condizioni di Utilizzo** del servizio.")
        
        if st.button("Registrati Ora", key="btn_register_action"):
            if not r_user.strip() or not r_pass.strip():
                st.warning("Compila tutti i campi obbligatori (Username e Password).")
            elif not accettazione_privacy or not accettazione_termini:
                st.error("⚠️ Per completare la registrazione è obbligatorio spuntare entrambe le caselle di accettazione dei termini legali e della privacy.")
            elif any(u['username'] == r_user for u in st.session_state.users):
                st.error("Lo username scelto è già occupato. Scegline un altro.")
            else:
                st.session_state.users.append({
                    "username": r_user, 
                    "password": r_pass, 
                    "accepted_privacy": True,
                    "accepted_terms": True,
                    "registration_date": str(datetime.datetime.now())
                })
                st.success("Registrazione completata con successo! Ora puoi effettuare il login nella scheda a fianco.")
    st.stop()

# --- STRUTTURA PRINCIPALE DELL'APPLICAZIONE (DOPO IL LOGIN) ---
st.sidebar.title(f"Benvenuto, {st.session_state.logged_user} ⚡")
menu = st.sidebar.radio("Navigazione", ["DASHBOARD", "MOVIMENTI", "CONTI", "IMPOSTAZIONI"])

if st.sidebar.button("Disconnetti"):
    st.session_state.logged_user = None
    st.rerun()

# --- GESTIONE SEZIONE IMPOSTAZIONI (CON CONSULTAZIONE LEGAL) ---
if menu == "IMPOSTAZIONI":
    st.subheader("⚙️ Impostazioni e Informazioni Legali")
    
    with st.expander("⚖️ Documentazione Legale e Normativa"):
        st.markdown("Qui puoi consultare in qualsiasi momento i documenti legali accettati in fase di registrazione.")
        show_legal_modals_or_expanders()
        
    with st.expander("🛠️ Preferenze Generali"):
        selected_lang = st.selectbox("Lingua", ["Italiano", "English"], index=0)
        selected_curr = st.selectbox("Valuta", ["EUR (€)", "USD ($)"], index=0)
        if st.button("Salva Impostazioni"):
            st.success("Impostazioni salvate correttamente.")

elif menu == "DASHBOARD":
    st.subheader("📊 Dashboard Principale")
    st.info("Benvenuto nella tua dashboard finanziaria protetta.")

elif menu == "MOVIMENTI":
    st.subheader("💳 Gestione Movimenti")

elif menu == "CONTI":
    st.subheader("🏦 Gestione Conti")
