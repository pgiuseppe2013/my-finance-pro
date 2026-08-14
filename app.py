import streamlit as st
import datetime

# --- CONFIGURAZIONE E STILE ---
st.set_page_config(page_title="MY FINANCE PRO", page_icon="⚡", layout="wide")

# --- INIZIALIZZAZIONE STATO ---
if 'users' not in st.session_state: st.session_state.users = []
if 'logged_user' not in st.session_state: st.session_state.logged_user = None

# --- TESTI LEGALI ESAUSTIVI (DA INSERIRE NEGLI EXPANDER) ---
def privacy_text_completa():
    st.markdown("""
    **INFORMATIVA SULLA PRIVACY (AI SENSI DEL GDPR - REGOLAMENTO UE 2016/679)**

    **1. Titolare del Trattamento**  
    Il Titolare del trattamento dei dati è lo sviluppatore e gestore della piattaforma MY FINANCE PRO.

    **2. Tipologia dei dati raccolti e finalità**  
    I dati personali raccolti al momento della registrazione comprendono: Indirizzo Email e Username. Vengono inoltre trattati i dati finanziari inseriti volontariamente dall'utente (movimenti, conti, importi, categorie). Tali dati sono trattati esclusivamente per consentire l'erogazione del servizio di gestione del bilancio personale e l'accesso all'area riservata.

    **3. Base giuridica del trattamento**  
    Il trattamento si fonda sul consenso esplicito prestato dall'utente mediante spunta in fase di registrazione e sulla necessità di eseguire il servizio richiesto.

    **4. Modalità di conservazione e Sicurezza**  
    I dati inseriti sono memorizzati all'interno dei sistemi di database dell'applicazione. Vengono adottate misure tecniche e organizzative adeguate a prevenire accessi non autorizzati, divulgazione, modifica o distruzione non autorizzata dei dati. Nessun dato viene ceduto a terzi per finalità commerciali o di profilazione.

    **5. Diritti dell'interessato**  
    L'utente gode in qualsiasi momento dei diritti di cui agli artt. 15 e seguenti del GDPR (accesso, rettifica, cancellazione, limitazione, opposizione al trattamento), esercitabili inviando una comunicazione al gestore della piattaforma o eliminando direttamente il proprio account.
    """)

def terms_text_completi():
    st.markdown("""
    **TERMINI E CONDIZIONI DI UTILIZZO DEL SERVIZIO**

    **1. Oggetto e Accettazione**  
    I presenti Termini e Condizioni regolano l'accesso e l'utilizzo del software MY FINANCE PRO. Completando la registrazione, l'utente accetta integralmente e senza riserve le presenti condizioni.

    **2. Natura del Software ed Esclusione di Responsabilità Finanziaria**  
    MY FINANCE PRO è uno strumento informatico di supporto alla gestione e catalogazione delle finanze personali fornito "così com'è" (as-is).  
    * **Il software NON fornisce consulenza finanziaria, fiscale, legale o di investimento.**  
    * Lo sviluppatore declina ogni responsabilità per eventuali errori di calcolo, perdite economiche, errata interpretazione dei dati o decisioni finanziarie intraprese dall'utente basandosi sui report generati dall'applicazione.

    **3. Responsabilità dell'Utente e Credenziali**  
    L'utente è l'unico ed esclusivo responsabile della custodia e della segretezza delle proprie credenziali di accesso (Username e Password). Qualsiasi attività compiuta tramite l'account registrato si intenderà effettuata dall'utente stesso. L'utente si impegna a manlevare e tenere indenne il gestore da qualsiasi pretesa derivante da un uso improprio o illecito del servizio.

    **4. Proprietà Intellettuale**  
    Tutti i diritti di proprietà intellettuale, il codice sorgente, la grafica, i loghi e i contenuti di MY FINANCE PRO sono di esclusiva proprietà del creatore. È severamente vietata la copia, la decompilazione, la redistribuzione o lo sfruttamento commerciale non autorizzato.

    **5. Modifiche e Sospensione del Servizio**  
    Il gestore si riserva il diritto di modificare, sospendere o interrompere, in tutto o in parte, il servizio in qualsiasi momento, anche senza preavviso, per esigenze tecniche, di sicurezza o legali, senza che ciò faccia sorgere alcun diritto dell'utente a risarcimenti o indennizzi.
    """)

# --- SCHERMATA LOGIN / REGISTRAZIONE ---
if not st.session_state.logged_user:
    st.title("🔐 MY FINANCE PRO - Accesso")
    tab_login, tab_register = st.tabs(["Accedi", "Registrati"])
    
    with tab_login:
        l_user = st.text_input("Username o Email", key="log_user")
        l_pass = st.text_input("Password", type="password", key="log_pass")
        if st.button("Accedi"):
            st.session_state.logged_user = l_user
            st.rerun()
                
    with tab_register:
        st.subheader("Crea il tuo Account")
        r_email = st.text_input("Inserisci la tua Email")
        r_user = st.text_input("Scegli uno Username")
        r_pass = st.text_input("Scegli una Password", type="password")
        
        st.markdown("---")
        
        # Testi nascosti dentro gli expander (l'utente li apre solo se vuole leggerli)
        with st.expander("📖 Leggi la Privacy Policy Completa (GDPR)"):
            privacy_text_completa()
            
        with st.expander("📖 Leggi i Termini e Condizioni di Servizio Completi"):
            terms_text_completi()
            
        # Due flag obbligatori puliti
        accetto_privacy = st.checkbox("Dichiaro di aver letto e accetto la Privacy Policy")
        accetto_termini = st.checkbox("Dichiaro di aver letto e accetto i Termini e Condizioni di Servizio")
        
        if st.button("Registrati"):
            if not r_email or not r_user or not r_pass:
                st.error("Tutti i campi (Email, Username, Password) sono obbligatori.")
            elif not accetto_privacy or not accetto_termini:
                st.error("Devi obbligatoriamente accettare sia la Privacy Policy che i Termini e Condizioni per registrarti.")
            else:
                st.session_state.users.append({"email": r_email, "username": r_user})
                st.success("Registrazione completata con successo! Ora puoi effettuare il login.")

    st.stop()

# --- AREA RISERVATA ---
st.sidebar.title(f"Bentornato {st.session_state.logged_user}")
if st.sidebar.button("Logout"):
    st.session_state.logged_user = None
    st.rerun()

st.title("Dashboard")
st.write("Area privata attiva.")
