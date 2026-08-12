import streamlit as st
import pandas as pd
import datetime
from datetime import date, timedelta
import plotly.express as px

# 1. CONFIGURAZIONE PAGINA & STILE TECH
st.set_page_config(page_title="MY FINANCE PRO", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #020617; color: #f8fafc; }
    .stButton>button {
        border-radius: 10px;
        background: linear-gradient(145deg, #16a34a, #15803d);
        color: white;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px rgba(34, 197, 94, 0.4);
        transform: translateY(-2px);
    }
    div[data-testid="stMetricValue"] { color: #22c55e; font-family: 'Urbanist', sans-serif; font-weight: 700; }
    .stDateInput input { background-color: #1e293b !important; color: white !important; border: 1px solid #334155 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. INIZIALIZZAZIONE STATO
if 'accounts' not in st.session_state:
    st.session_state.accounts = []
if 'movements' not in st.session_state:
    st.session_state.movements = []
if 'settings' not in st.session_state:
    st.session_state.settings = {"lang": "IT", "currency": "EUR"}

LANGS = ["IT", "EN", "FR", "ES", "DE", "PT", "ZH", "JA", "RU", "AR"]
CURRS = ["EUR", "USD", "GBP", "CHF", "JPY", "CAD", "AUD", "CNY", "INR", "BRL"]
CATS_IN = ["Stipendio", "Rendita", "Bonus", "Vendita", "Altro"]
CATS_OUT = ["Affitto", "Mutuo", "Utenze", "Supermercato", "Shopping", "Trasporti", "Salute", "Svago"]

# 3. FUNZIONI LOGICHE SMART
def add_movement(m_date_c, m_date_v, acc_id, m_type, cat, desc, amt):
    acc = next((a for a in st.session_state.accounts if a['id'] == acc_id), None)
    if acc and acc['type'] == "Carta di Credito" and amt < 0:
        next_month = m_date_c.replace(day=1) + timedelta(days=32)
        addebito_date = next_month.replace(day=acc.get('addebito_day', 1))
        st.session_state.movements.append({
            "id": f"PREV_{datetime.datetime.now().timestamp()}",
            "date_c": addebito_date, "date_v": addebito_date,
            "acc_id": acc_id, "type": "Uscita (Prev)", "cat": "Saldo Carta",
            "desc": f"Addebito previsto: {desc}", "amt": amt, "virtual": True
        })
    
    st.session_state.movements.append({
        "id": str(datetime.datetime.now().timestamp()),
        "date_c": m_date_c, "date_v": m_date_v,
        "acc_id": acc_id, "type": m_type, "cat": cat,
        "desc": desc, "amt": amt, "virtual": False
    })

# 4. NAVIGAZIONE
menu = st.sidebar.selectbox("MENU", ["DASHBOARD", "MOVIMENTI", "REPORT (CASH FLOW)", "IMPOSTAZIONI"])

# --- DASHBOARD ---
if menu == "DASHBOARD":
    st.title("⚡ DASHBOARD FINANZIARIA")
    
    total_cash = sum(a['init_bal'] + sum(m['amt'] for m in st.session_state.movements if m['acc_id'] == a['id'] and not m.get('virtual')) for a in st.session_state.accounts if a['type'] != "Carta di Credito")
    st.metric("LIQUIDITÀ TOTALE", f"{total_cash:,.2f} {st.session_state.settings['currency']}")

    cols = st.columns(3)
    for i, acc in enumerate(st.session_state.accounts):
        with cols[i % 3]:
            with st.container(border=True):
                bal = acc['init_bal'] + sum(m['amt'] for m in st.session_state.movements if m['acc_id'] == acc['id'] and not m.get('virtual'))
                st.subheader(f"{acc['name']}")
                st.write(f"Tipo: {acc['type']}")
                if acc['type'] == "Carta di Credito":
                    used = abs(sum(m['amt'] for m in st.session_state.movements if m['acc_id'] == acc['id'] and m['amt'] < 0))
                    residuo = acc['plafond'] - used
                    st.metric("Residuo Plafond", f"{residuo:,.2f}")
                    st.progress(residuo / acc['plafond'] if acc['plafond'] > 0 else 0)
                else:
                    st.metric("Saldo Attuale", f"{bal:,.2f}")
                
                if st.button("Elimina", key=f"del_{acc['id']}"):
                    st.session_state.accounts = [a for a in st.session_state.accounts if a['id'] != acc['id']]
                    st.rerun()

    with st.expander("➕ AGGIUNGI NUOVO CONTO / CARTA"):
        t = st.selectbox("Tipo", ["Bancario", "Prepagata", "Carta di Credito"])
        name = st.text_input("Nome")
        init = st.number_input("Saldo di partenza", value=0.0)
        plafond = 0.0
        addebito = 1
        if t == "Carta di Credito":
            plafond = st.number_input("Plafond Mensile", value=1500.0)
            addebito = st.slider("Giorno Addebito (Mese Succ)", 1, 28, 1)
        
        if st.button("CREA"):
            new_id = str(datetime.datetime.now().timestamp())
            st.session_state.accounts.append({
                "id": new_id, "name": name, "type": t, 
                "init_bal": init, "plafond": plafond, "addebito_day": addebito
            })
            st.rerun()

# --- MOVIMENTI ---
elif menu == "MOVIMENTI":
    st.title("📝 LISTA MOVIMENTI")
    
    if not st.session_state.accounts:
        st.warning("Crea prima almeno un conto o una carta dalla Dashboard!")
    else:
        with st.container(border=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                dc = st.date_input("Data Contabile", key="dc")
            with c2:
                dv = st.date_input("Data Valuta", value=dc, key="dv")
            with c3:
                acc_choice = st.selectbox("Conto", [a['name'] for a in st.session_state.accounts])
            
            c4, c5, c6 = st.columns(3)
            with c4:
                m_type = st.radio("Tipo", ["Entrata", "Uscita"], horizontal=True)
            with c5:
                cats = CATS_IN if m_type == "Entrata" else CATS_OUT
                cat = st.selectbox("Categoria", cats)
            with c6:
                amt = st.number_input("Importo", min_value=0.01)
                if m_type == "Uscita": amt = -amt
            
            desc = st.text_input("Descrizione (Opt)")
            if st.button("INSERISCI MOVIMENTO"):
                a_id = next(a['id'] for a in st.session_state.accounts if a['name'] == acc_choice)
                add_movement(dc, dv, a_id, m_type, cat, desc, amt)
                st.success("Inserito!")
                st.rerun()

    st.divider()
    search = st.text_input("Cerca nei movimenti...")
    df = pd.DataFrame(st.session_state.movements)
    if not df.empty:
        df_show = df[df['virtual'] == False]
        if search:
            df_show = df_show[df_show['desc'].str.contains(search, case=False)]
        st.dataframe(df_show, use_container_width=True)

# --- REPORT ---
elif menu == "REPORT (CASH FLOW)":
    st.title("📊 ANALISI CASH FLOW")
    d_range = st.date_input("Periodo", [date.today() - timedelta(days=30), date.today() + timedelta(days=30)])
    
    if len(d_range) == 2:
        df = pd.DataFrame(st.session_state.movements)
        if not df.empty:
            df['date_c'] = pd.to_datetime(df['date_c']).dt.date
            mask = (df['date_c'] >= d_range[0]) & (df['date_c'] <= d_range[1])
            df_filtered = df[mask]
            
            e = df_filtered[df_filtered['amt'] > 0]['amt'].sum()
            u = df_filtered[df_filtered['amt'] < 0]['amt'].sum()
            c1, c2, c3 = st.columns(3)
            c1.metric("Entrate", f"{e:,.2f}")
            c2.metric("Uscite", f"{u:,.2f}")
            c3.metric("Netto", f"{e+u:,.2f}")
            
            fig = px.area(df.sort_values('date_c'), x='date_c', y='amt', title="Trend Cash Flow (Incl. Previsioni)", template="plotly_dark")
            fig.update_traces(line_color='#22c55e')
            st.plotly_chart(fig, use_container_width=True)

# --- IMPOSTAZIONI ---
elif menu == "IMPOSTAZIONI":
    st.title("⚙️ IMPOSTAZIONI")
    st.session_state.settings['lang'] = st.selectbox("Lingua", LANGS)
    st.session_state.settings['currency'] = st.selectbox("Valuta", CURRS)
    if st.button("SALVA & REFRESH"):
        st.rerun()
