# --- GESTIONE AUTENTICAZIONE E UTENTI ---
if 'users' not in st.session_state:
    st.session_state.users = []  # Lista dizionari: {"username": ..., "password": ...}
if 'logged_user' not in st.session_state:
    st.session_state.logged_user = None

# Se l'utente non è loggato, mostra la schermata di accesso/registrazione
if not st.session_state.logged_user:
    st.title("🔐 Accesso a MY FINANCE PRO")
    tab_login, tab_register = st.tabs(["Accedi", "Crea un nuovo account"])
    
    with tab_login:
        l_user = st.text_input("Username", key="login_user")
        l_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            user_found = next((u for u in st.session_state.users if u['username'] == l_user and u['password'] == l_pass), None)
            if user_found:
                st.session_state.logged_user = l_user
                st.success(Accesso effettuato con successo!)
                st.rerun()
            else:
                st.error("Credenziali non valide o account inesistente.")
                
    with tab_register:
        r_user = st.text_input("Scegli uno Username", key="reg_user")
        r_pass = st.text_input("Scegli una Password", type="password", key="reg_pass")
        if st.button("Registrati"):
            if not r_user.strip() or not r_pass.strip():
                st.warning("Inserisci username e password validi.")
            elif any(u['username'] == r_user for u in st.session_state.users):
                st.error("Questo username è già occupato.")
            else:
                st.session_state.users.append({"username": r_user, "password": r_pass})
                st.success("Account creato con successo! Ora puoi effettuare il login.")
    
    # Interrompiamo l'esecuzione del resto dell'app finché non c'è il login
    st.stop()
