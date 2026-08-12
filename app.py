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

# 3. FUNZIONE LOGICA CALCOLO SALDO CON DATA DI CUT-OFF
def get_account_balance(acc):
    acc_id = acc['id']
    init_bal = acc['init_bal']
    init_date = acc.get('init_date', date.min)
    
    valid_movements = [
        m for m in st.session_state.movements 
        if m['acc_id'] == acc_id and not m.get('virtual') and pd.to_datetime(m['date_c']).date() >= init_date
    ]
    
    return init_bal + sum(m['amt'] for m in valid_movements)

# 4. FUNZIONE AGGIUNTA MOVIMENTO
def add_movement(m_date_c, m_date_v, acc_id, m_type, cat, desc, amt):
    acc = next((a for a in st.session_state.accounts if a['id'] == acc_id), None)
    
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

# 5. WIDGET MOVIMENTO DIETRO "+" CON SINCRONIZZAZIONE DATE UNIDIREZIONALE
def render_movement_form(key_suffix=""):
    with st.expander("➕ Aggiungi Nuovo Movimento"):
        if not st.session_state.accounts:
            st.warning("⚠️ Crea prima almeno un Conto o una Carta di Credito dalla Dashboard per poter inserire movimenti.")
            return

        dc_key = f"dc_input_{key_suffix}"
        dv_key = f"dv_input_{key_suffix}"
        last_dc_key = f"last_dc_{key_suffix}"
        
        # Inizializzazione date nello stato se non esistono
        if dc_key not in st.session_state:
            st.session_state[dc_key] = date.today()
        if dv_key not in st.session_state:
            st.session_state[dv_key] = date.today()
        if last_dc_key not in st.session_state:
            st.session_state[last_dc_key] = st.session_state[dc_key]

        col1, col2, col3 = st.columns(3)
        with col1:
            dc = st.date_input("Data Contabile", key=dc_key)
            
        # Logica di sincronizzazione: se la data contabile è cambiata rispetto all'ultimo controllo, aggiorna la valuta
        if dc != st.session_state[last_dc_key]:
            st.session_state[dv_key] = dc
            st.session_state[last_dc_key] = dc

        with col2:
            dv = st.date_input("Data Valuta", key=dv_key)
        with col3:
            acc_choice = st.selectbox("Seleziona Conto / Carta", [a['name'] for a in st.session_state.accounts], key=f"acc_sel_{key_suffix}")

        col4, col5, col6 = st.columns(3)
        with col4:
            m_type = st.radio("Tipo Operazione", ["Entrata", "Uscita"], horizontal=True, key=f"m_type_{key_suffix}")
        with col5:
            cats = CATS_IN if m_type == "Entrata" else CATS_OUT
            cat = st.selectbox("Categoria", cats, key=f"cat_{key_suffix}")
        with col6:
            amt = st.number_input("Importo", min_value=0.01, step=1.0, key=f"amt_{key_suffix}")
            if m_type == "Uscita": amt = -amt

        desc = st.text_input("Descrizione (Opzionale)", key=f"desc_{key_suffix}")

        if st.button("REGISTRA MOVIMENTO", key=f"btn_save_mov_{key_suffix}"):
            a_id = next(a['id'] for a in st.session_state.accounts if a['name'] == acc_choice)
            add_movement(dc, dv, a_id, m_type, cat, desc, amt)
            st.success("✅ Movimento registrato con successo!")
            st.rerun()

# 6. BARRA DI NAVIGAZIONE A PULSANTI
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
    st.subheader("Panoramica Patrimoniale e Conti")
    
    total_cash = sum(get_account_balance(a) for a in st.session_state.accounts if a['type'] != "Carta di Credito")
    st.metric("LIQUIDITÀ TOTALE", f"{total_cash:,.2f} {st.session_state.settings['currency']}")

    cols = st.columns(3)
    for i, acc in enumerate(st.session_state.accounts):
        with cols[i % 3]:
            with st.container(border=True):
                bal = get_account_balance(acc)
                st.markdown(f"### {acc['name']}")
                st.caption(f"Tipo: {acc['type']} | Dal: {acc.get('init_date', date.today()).strftime('%d/%m/%Y') if acc['type'] != 'Carta di Credito' else 'N/D'}")
                
                if acc['type'] == "Carta di Credito":
                    used = abs(sum(m['amt'] for m in st.session_state.movements if m['acc_id'] == acc['id'] and m['amt'] < 0 and not m.get('virtual')))
                    residuo = acc['plafond'] - used
                    st.metric("Residuo Plafond", f"{residuo:,.2f}")
                    st.caption(f"Scadenza: {acc.get('scadenza', 'N/D')}")
                    st.progress(residuo / acc['plafond'] if acc['plafond'] > 0 else 0)
                else:
                    st.metric("Saldo Attuale", f"{bal:,.2f}")
                
                if st.button("Elimina Conto", key=f"del_{acc['id']}"):
                    st.session_state.accounts = [a for a in st.session_state.accounts if a['id'] != acc['id']]
                    st.rerun()

    st.divider()

    # Form inserimento Conto/Carta nascosta dietro un "+" (Expander)
    with st.expander("➕ Aggiungi Nuovo Conto o Carta"):
        t = st.selectbox("Tipo di Rapporto", ["Bancario", "Prepagata", "Carta di Credito"])
        name = st.text_input("Nome Conto / Carta", key="acc_name_dash")
        
        init = 0.0
        init_date = date.today()
        plafond = 0.0
        addebito = 1
        scadenza = date.today() + timedelta(days=365)
        
        if t == "Carta di Credito":
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                plafond = st.number_input("Plafond Mensile", value=1500.0, step=100.0, key="acc_plafond_dash")
            with col_p2:
                scadenza = st.date_input("Data Scadenza Carta", value=scadenza, key="acc_scad_dash")
            with col_p3:
                addebito = st.slider("Giorno Addebito", 1, 28, 1, key="acc_add_dash")
        else:
            col_i1, col_i2 = st.columns(2)
            with col_i1:
                init = st.number_input("Saldo di Partenza", value=0.0, step=100.0, key="acc_init_dash")
            with col_i2:
                init_date = st.date_input("A che data hai questo saldo?", value=date.today(), key="acc_init_date_dash")
        
        if st.button("CREA CONTO / CARTA", key="btn_create_acc_dash"):
            if name.strip() == "":
                st.warning("Inserisci un nome valido per il conto.")
            else:
                new_id = str(datetime.datetime.now().timestamp())
                st.session_state.accounts.append({
                    "id": new_id, "name": name, "type": t, 
                    "init_bal": init, "init_date": init_date, 
                    "plafond": plafond, "addebito_day": addebito,
                    "scadenza": scadenza.strftime("%d/%m/%Y") if t == "Carta di Credito" else ""
                })
                st.success("✅ Conto creato con successo!")
                st.rerun()

# --- MOVIMENTI ---
elif menu == "MOVIMENTI":
    st.subheader("Gestione Movimenti")
    render_movement_form(key_suffix="mov_tab")

    st.divider()
    search = st.text_input("🔍 Cerca nei movimenti...", key="search_mov")
    df = pd.DataFrame(st.session_state.movements)
    if not df.empty:
        df_show = df[df['virtual'] == False]
        if search:
            df_show = df_show[df_show['desc'].str.contains(search, case=False)]
        st.dataframe(df_show, use_container_width=True)

# --- REPORT ---
elif menu == "REPORT":
    st.subheader("Analisi Cash Flow e Dettagli")
    render_movement_form(key_suffix="rep_tab")

    st.divider()
    d_range = st.date_input("Seleziona Periodo Analisi (Passato & Futuro)", [date.today() - timedelta(days=90), date.today() + timedelta(days=90)], key="report_range")
    
    if len(d_range) == 2:
        initial_total_balance = sum(a['init_bal'] for a in st.session_state.accounts if a['type'] != "Carta di Credito")
        
        df = pd.DataFrame(st.session_state.movements)
        if not df.empty:
            df['date_c'] = pd.to_datetime(df['date_c']).dt.date
            
            valid_rows = []
            for _, row in df.iterrows():
                acc = next((a for a in st.session_state.accounts if a['id'] == row['acc_id']), None)
                if acc and acc['type'] != "Carta di Credito":
                    cutoff = acc.get('init_date', date.min)
                    if row['date_c'] >= cutoff or row.get('virtual'):
                        valid_rows.append(row)
                else:
                    valid_rows.append(row)
            
            df_valid = pd.DataFrame(valid_rows) if valid_rows else pd.DataFrame(columns=df.columns)
            
            if not df_valid.empty:
                df_sorted = df_valid.sort_values('date_c').copy()
                df_sorted['cumulative_flow'] = initial_total_balance + df_sorted['amt'].cumsum()
                
                mask = (df_sorted['date_c'] >= d_range[0]) & (df_sorted['date_c'] <= d_range[1])
                df_filtered = df_sorted[mask]
                
                e = df_filtered[df_filtered['amt'] > 0]['amt'].sum()
                u = df_filtered[df_filtered['amt'] < 0]['amt'].sum()
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Totale Entrate", f"{e:,.2f}")
                c2.metric("Totale Uscite", f"{u:,.2f}")
                c3.metric("Flusso Netto Periodo", f"{e+u:,.2f}")
                
                fig = px.area(df_filtered, x='date_c', y='cumulative_flow', title="Trend Cash Flow Patrimoniale", template="plotly_dark", labels={'cumulative_flow': 'Patrimonio Totale', 'date_c': 'Data'})
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
    render_movement_form(key_suffix="set_tab")

    st.divider()
    st.session_state.settings['lang'] = st.selectbox("Lingua", LANGS, index=LANGS.index(st.session_state.settings['lang']))
    st.session_state.settings['currency'] = st.selectbox("Valuta", CURRS, index=CURRS.index(st.session_state.settings['currency']))
    if st.button("SALVA IMPOSTAZIONI", key="btn_save_set"):
        st.success("✅ Impostazioni salvate!")
        st.rerun()
