import streamlit as st
import yfinance as yf
import pandas as pd

# Configurazione Pagina
st.set_page_config(page_title="Trading Pro Dashboard", layout="wide")

st.title("🚀 Trading Pro Dashboard")
st.markdown("---")

# --- SIDEBAR: GESTIONE CAPITALE ---
st.sidebar.header("💰 Gestione Capitale")
capitale = st.sidebar.number_input("Capitale Totale (€)", min_value=0.0, value=1000.0, step=100.0)
rischio_percent = st.sidebar.slider("Rischio per operazione (%)", 0.1, 5.0, 1.0)
rischio_euro = capitale * (rischio_percent / 100)

st.sidebar.write(f"**Rischio massimo per trade:** {rischio_euro:.2f} €")
st.markdown("---")

# --- SEZIONE 1: ANALISI REAL-TIME ---
st.subheader("🔍 Analisi Asset in Tempo Reale")
col1, col2 = st.columns([1, 2])

with col1:
    asset = st.text_input("Inserisci Simbolo (es: NVDA, BTC-USD, GC=F per Oro)", "NVDA")
    try:
        ticker = yf.Ticker(asset)
        prezzo_attuale = ticker.history(period="1d")['Close'].iloc[-1]
        st.metric(label=f"Prezzo Attuale {asset}", value=f"{prezzo_attuale:.2f}")
    except:
        st.error("Simbolo non trovato. Verifica il ticker (es. BTC-USD per Bitcoin).")
        prezzo_attuale = None

if prezzo_attuale:
    with col2:
        st.write("### 🛠️ Calcolo Punti di Ingresso")
        supporto = st.number_input("Prezzo di Supporto (Compra qui)", value=float(prezzo_attuale * 0.95))
        resistenza = st.number_input("Prezzo di Resistenza (Vendi qui)", value=float(prezzo_attuale * 1.05))
        
        # Logica di Segnale
        if prezzo_attuale <= supporto:
            st.success("✅ SEGNALE: ACQUISTA (Prezzo in zona supporto)")
        elif prezzo_attuale >= resistenza:
            st.error("🚨 SEGNALE: VENDI (Prezzo in zona resistenza)")
        else:
            st.warning("⏳ SEGNALE: ATTENDI (Prezzo in zona neutra)")

st.markdown("---")

# --- SEZIONE 2: CALCOLO POSIZIONE (RISK MANAGEMENT) ---
if prezzo_attuale:
    st.subheader("📏 Calcolo Dimensione Posizione")
    stop_loss = st.number_input("Inserisci il tuo Stop Loss (€)", value=float(prezzo_attuale * 0.90))
    
    distanza_stop = prezzo_attuale - stop_loss
    
    if distanza_stop > 0:
        quantita = rischio_euro / distanza_stop
        valore_posizione = quantita * prezzo_attuale
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Quantità da comprare", f"{quantita:.4f}")
        c2.metric("Valore Totale Posizione", f"{valore_posizione:.2f} €")
        c3.metric("Rischio Fisso", f"{rischio_euro:.2f} €")
    else:
        st.error("Lo Stop Loss deve essere inferiore al prezzo attuale!")

st.markdown("---")

# --- SEZIONE 3: DIARIO PROFITTI SEMPLICE ---
st.subheader("📈 Calcolo Profitti Operazione")
with st.expander("Apri Calcolatore Profitto"):
    p_entrata = st.number_input("Prezzo Entrata", value=0.0)
    p_uscita = st.number_input("Prezzo Uscita", value=0.0)
    q_detta = st.number_input("Quantità posseduta", value=0.0)
    
    if p_entrata > 0 and p_uscita > 0:
        profitto = (p_uscita - p_entrata) * q_detta
        percentuale = ((p_uscita - p_entrata) / p_entrata) * 100
        st.write(f"**Profitto Netto:** {profitto:.2f} €")
        st.write(f"**Variazione:** {percentuale:.2f}%")
