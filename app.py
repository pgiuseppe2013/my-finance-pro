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
    </style>
    """, unsafe_allow_html=True)

# 2. INIZIALIZZAZIONE STATO
if 'accounts' not in st.session_state:
    st.session_state.accounts = []
if 'movements' not in st.session_state:
    st.session_state.movements = []
if 'settings' not in st.session_state:
    st.session_state.settings = {"lang": "IT", "currency": "EUR"}
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "DASHBOARD"

LANGS = ["IT", "EN", "FR", "ES", "DE", "PT", "ZH", "JA", "RU", "AR"]
CURRS = ["EUR", "USD", "GBP", "CHF", "JPY", "CAD", "AUD", "CNY", "INR", "BRL"]
CATS_IN = ["Stipendio", "Rendita", "Bonus", "Vendita", "Altro"]
CATS_OUT = ["Affitto", "Mutuo", "Utenze", "Supermercato", "Shopping", "Trasporti", "Salute", "Svago"]

# 3. FUNZIONI LOGICHE SMART CON GESTIONE CARTA CORRETTA
def add_movement(m_date_c, m_date_v, acc_id, m_type, cat, desc, amt):
    acc = next((a for a in st.session_state.accounts if a['id'] == acc_id), None)
    
    # Se è una spesa con Carta di Credito, generiamo il movimento revisionale di addebito al mese successivo
    if acc and acc['type'] == "Carta di Credito" and amt < 0:
        try:
            next_month = m_date_c.replace(day=1) + timedelta(days=32)
            addebito_date = next_month.replace(day=acc.get('addebito_day', 1))
        except ValueError:
            addebito_date = m_date_c + timedelta(days=30)
            
        st.session_state.movements.append({
            "id": f"PREV_{datetime.datetime.now().timestamp()}",
            "date_c": addebito_date, "date_v": addebito_date,
            "acc_id": acc_id, "type": "Uscita (Prev)", "cat": "Saldo Carta",
            "desc": f"Addebito carta: {desc}", "amt": amt, "virtual": True
        })
    
    st.session_state.movements.append({
        "id": str(datetime.datetime.now().timestamp()),
        "date_c": m_date_c, "date_v": m_date_v,
        "acc_id": acc_id, "type": m_type, "cat": cat,
        "desc": desc, "amt": amt, "virtual": False
    })

# 4. BARRA DI NAVIGAZIONE A PULSANTI PRONTI
st.title("⚡ MY FINANCE PRO")
b1, b2, b3, b4 = st.columns(4)
with b1:
    if st.button("📊 DASHBOARD", use_container_width=True): st.session_state.active_tab = "DASHBOARD"
with b2:
    if st.button("📝 MOVIMENTI", use_container_width=True): st.session_state.active_tab = "MOVIMENTI"
with b3:
    if st.button("📈 REPORT & CASH FLOW", use_container_width=True): st.session_state.active_tab = "REPORT"
with b4:
    if st.button("⚙️ IMPOSTAZIONI", use_container_width=True): st.session_state.active_tab = "IMPOSTAZIONI"

st.divider()
menu = st.session_state.active_tab

# --- DASHBOARD ---
if menu == "DASHBOARD":
    st.subheader("Panoramica Patrimoniale")
    
    total_cash = sum(a['init_bal'] + sum(m['amt'] for m in st.session_state.movements if m['acc_id'] == a['id'] and not m.get('virtual')) for a in st.session_state.accounts if a['type'] != "Carta di Credito")
    st.metric("LIQUIDITÀ TOTALE", f"{total_cash:,.2f} {st.session_state.settings['currency']}")

    cols = st.columns(3)
    for i, acc in enumerate(st.session_state.accounts):
        with cols[i % 3]:
            with st.container(border=True):
                bal = acc['init_bal'] + sum(m['amt'] for m in st.session_state.movements if m['acc_id'] == acc['id'] and not m.get('virtual'))
                st.markdown(f"### {acc['name']}")
                st.caption(f"Tipo: {acc['type']}")
                if acc['type'] == "Carta di Credito":
                    used = abs(sum(m['amt'] for m in st.session_state.movements if m['acc_id'] == acc['id'] and m['amt'] < 0))
                    residuo = acc['plafond'] - used
                    st.metric("Residuo Plafond", f"{residuo:,.2f}")
                    st.caption(f"Scadenza: {acc.get('scadenza', 'N/D')}")
                    st.progress(residuo / acc['plafond'] if acc['plafond'] > 0 else 0)
                else:
                    st.metric("Saldo Attuale", f"{bal:,.2f}")
                
                if st.button("Elimina", key=f"del_{acc['id']}"):
                    st.session_state.accounts = [a for a in st.session_state.accounts if a['id'] != acc['id']]
                    st.rerun()

    st.divider()
    
    # Inserimento rapido movimento direttamente dalla Dashboard
    st.subheader("⚡ Inserimento Rapido Movimento")
    if not st.session_state.accounts:
        st.info("Crea prima almeno un conto o carta qui sotto per registrare movimenti.")
    else:
        with st.container(border=True):
            dc_dash = st.date_input("Data Contabile", key="dc_dash")
            dv_dash = st.date_input("Data Valuta", value=dc_dash, key="dv_dash")
            acc_choice_d = st.selectbox("Conto", [a['name'] for a in st.session_state.accounts], key="acc_d")
            
            c_t1, c_t2, c_t3 = st.columns(3)
            with c_t1:
                m_type_d = st.radio("Tipo", ["Entrata", "Uscita"], horizontal=True, key="m_type_d")
            with c_t2:
                cats_d = CATS_IN if m_type_d == "Entrata" else CATS_OUT
                cat_d = st.selectbox("Categoria", cats_d, key="cat_d")
            with c_t3:
                amt_d = st.number_input("Importo", min_value=0.01, key="amt_d")
                if m_type_d == "Uscita": amt_d = -amt_d
            
            desc_d = st.text_input("Descrizione (Opzionale)", key="desc_d")
            if st.button("REGISTRA MOVIMENTO (DASHBOARD)", key="btn_reg_dash"):
                a_id = next(a['id'] for a in st.session_state.accounts if a['name'] == acc_choice_d)
                add_movement(dc_dash, dv_dash, a_id, m_type_d, cat_d, desc_d, amt_d)
                st.success("Movimento registrato con successo!")
                st.rerun()

    st.divider()
    with st.expander("➕ AGGIUNGI NUOVO CONTO / CARTA"):
        t = st.selectbox("Tipo", ["Bancario", "Prepagata", "Carta di Credito"])
        name = st.text_input("Nome Conto / Carta", key="new_acc_name")
        
        init = 0.0
        plafond = 0.0
        addebito = 1
        scadenza = date.today() + timedelta(days=365)
        
        if t == "Carta di Credito":
            plafond = st.number_input("Plafond Mensile", value=1500.0, key="new_acc_plafond")
            scadenza = st.date_input("Data di Scadenza Carta", value=scadenza, key="new_acc_scad")
            addebito = st.slider("Giorno Addebito (Mese Succ)", 1, 28, 1, key="new_acc_add")
        else:
            init = st.number_input("Saldo di partenza", value=0.0, key="new_acc_init")
        
        if st.button("CREA CONTO / CARTA", key="btn_create_acc"):
            new_id = str(datetime.datetime.now().timestamp())
            st.session_state.accounts.append({
                "id": new_id, "name": name, "type": t, 
                "init_bal": init, "plafond": plafond, "addebito_day": addebito,
                "scadenza": scadenza.strftime("%d/%m/%Y") if t == "Carta di Credito" else ""
            })
            st.success("Creato con successo!")
            st.rerun()

# --- MOVIMENTI ---
elif menu == "MOVIMENTI":
    st.subheader("Gestione Movimenti")
    
    if not st.session_state.accounts:
        st.warning("Crea prima almeno un conto o una carta dalla Dashboard!")
    else:
        with st.container(border=True):
            if 'last_dc' not in st.session_state:
                st.session_state.last_dc = date.today()
            if 'last_dv' not in st.session_state:
                st.session_state.last_dv = date.today()

            c1, c2, c3 = st.columns(3)
            with c1:
                dc = st.date_input("Data Contabile", key="dc_main")
            with c2:
                if dc != st.session_state.last_dc:
                    st.session_state.last_dv = dc
                    st.session_state.last_dc = dc
                dv = st.date_input("Data Valuta", value=st.session_state.last_dv, key="dv_main")
                if dv != st.session_state.last_dv:
                    st.session_state.last_dv = dv
            with c3:
                acc_choice = st.selectbox("Conto", [a['name'] for a in st.session_state.accounts], key="acc_main")
            
            c4, c5, c6 = st.columns(3)
            with c4:
                m_type = st.radio("Tipo", ["Entrata", "Uscita"], horizontal=True, key="m_type_main")
            with c5:
                cats = CATS_IN if m_type == "Entrata" else CATS_OUT
                cat = st.selectbox("Categoria", cats, key="cat_main")
            with c6:
                amt = st.number_input("Importo", min_value=0.01, key="amt_main")
                if m_type == "Uscita": amt = -amt
            
            desc = st.text_input("Descrizione (Opzionale)", key="desc_main")
            if st.button("INSERISCI MOVIMENTO", key="btn_ins_mov"):
                a_id = next(a['id'] for a in st.session_state.accounts if a['name'] == acc_choice)
                add_movement(dc, dv, a_id, m_type, cat, desc, amt)
                st.success("Movimento inserito con successo!")
                st.rerun()

    st.divider()
    search = st.text_input("🔍 Cerca nei movimenti...", key="search_mov")
    df = pd.DataFrame(st.session_state.movements)
    if not df.empty:
        df_show = df[df['virtual'] == False]
        if search:
            df_show = df_show[df_show['desc'].str.contains(search, case=False)]
        st.dataframe(df_show, use_container_width=True)

# --- REPORT (CASH FLOW COMPLETO CON SALDI INIZIALI E PREVISIONI) ---
elif menu == "REPORT":
    st.subheader("Analisi Cash Flow e Dettagli")
    d_range = st.date_input("Seleziona Periodo Analisi", [date.today() - timedelta(days=90), date.today() + timedelta(days=90)], key="report_range")
    
    if len(d_range) == 2:
        # Calcoliamo il saldo patrimoniale iniziale totale dei conti non carta
        initial_total_balance = sum(a['init_bal'] for a in st.session_state.accounts if a['type'] != "Carta di Credito")
        
        df = pd.DataFrame(st.session_state.movements)
        if not df.empty:
            df['date_c'] = pd.to_datetime(df['date_c']).dt.date
            
            # Ordiniamo per data per calcolare l'andamento progressivo (Cash Flow cumulata)
            df_sorted = df.sort_values('date_c').copy()
            df_sorted['cumulative_flow'] = initial_total_balance + df_sorted['amt'].cumsum()
            
            mask = (df_sorted['date_c'] >= d_range[0]) & (df_sorted['date_c'] <= d_range[1])
            df_filtered = df_sorted[mask]
            
            e = df_filtered[df_filtered['amt'] > 0]['amt'].sum()
            u = df_filtered[df_filtered['amt'] < 0]['amt'].sum()
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Totale Entrate", f"{e:,.2f}")
            c2.metric("Totale Uscite", f"{u:,.2f}")
            c3.metric("Flusso Netto Periodo", f"{e+u:,.2f}")
            
            # Grafico del Cash Flow basato sulla liquidità complessiva comprensiva dei saldi bancari
            fig = px.area(df_filtered, x='date_c', y='cumulative_flow', title="Trend Cash Flow Patrimoniale (Incl. Saldi Iniziali e Previsioni)", template="plotly_dark", labels={'cumulative_flow': 'Patrimonio Totale', 'date_c': 'Data'})
            fig.update_traces(line_color='#22c55e', fillcolor='rgba(34, 197, 94, 0.2)')
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### 🔍 Dettaglio Movimenti per Categoria")
            filter_mode = st.radio("Fissa vista dettaglio:", ["Tutti", "Solo Entrate", "Solo Uscite"], horizontal=True, key="filter_mode")
            
            if filter_mode == "Solo Entrate":
                df_detail = df_filtered[df_filtered['amt'] > 0]
            elif filter_mode == "Solo Uscite":
                df_detail = df_filtered[df_filtered['amt'] < 0]
            else:
                df_detail = df_filtered
                
            st.dataframe(df_detail[['date_c', 'date_v', 'type', 'cat', 'desc', 'amt']], use_container_width=True)

# --- IMPOSTAZIONI ---
elif menu == "IMPOSTAZIONI":
    st.subheader("Configurazioni App")
    st.session_state.settings['lang'] = st.selectbox("Lingua", LANGS, index=LANGS.index(st.session_state.settings['lang']))
    st.session_state.settings['currency'] = st.selectbox("Valuta", CURRS, index=CURRS.index(st.session_state.settings['currency']))
    if st.button("SALVA IMPOSTAZIONI", key="btn_save_set"):
        st.success("Impostazioni salvate!")
        st.rerun()
