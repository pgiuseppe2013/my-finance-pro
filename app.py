import streamlit as st

# Configurazione della pagina
st.set_page_config(page_title="MY FINANCE PRO", page_icon="💰", layout="centered")

# Titolo principale
st.title("💰 MY FINANCE PRO")
st.write("Benvenuto nella tua app finanziaria personale!")

# Menu di navigazione laterale
menu = st.sidebar.selectbox("Seleziona Sezione", ["Dashboard", "Movimenti", "Impostazioni"])

if menu == "Dashboard":
    st.subheader("📊 Panoramica Conti")
    st.info("Qui vedrai presto i tuoi conti e i saldi aggiornati.")
    
    # Esempio di input rapido per testare
    st.markdown("---")
    st.write("Aggiungi una spesa veloce di prova:")
    importo = st.number_input("Importo (€)", min_value=0.0, step=1.0)
    if st.button("Registra Spesa"):
        st.success(f"Registrata spesa di {importo} €!")

elif menu == "Movimenti":
    st.subheader("📝 Elenco Movimenti")
    st.write("Qui apparirà la lista di tutte le tue entrate e uscite.")

elif menu == "Impostazioni":
    st.subheader("⚙️ Impostazioni App")
    lingua = st.selectbox("Lingua App", ["Italiano", "English"])
    valuta = st.selectbox("Valuta", ["EUR (€)", "USD ($)"])
    if st.button("Salva Impostazioni"):
        st.success("Impostazioni salvate con successo!")