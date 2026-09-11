import json
import os
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Climbing Logbook & Stats", page_icon="🧗‍♂️", layout="wide"
)

# Inizializzazione cartelle e file dati
os.makedirs("data", exist_ok=True)
ASCENTS_FILE = "data/ascents.json"
VIE_LUNGHE_FILE = "data/vie_lunghe.json"
PROGETTI_FILE = "data/progetti.json"


def load_json(filepath):
  if os.path.exists(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
      return json.load(f)
  return []


def save_json(filepath, data):
  with open(filepath, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)


# Sidebar di Navigazione
st.sidebar.title("🧗‍♂️ Climbing Hub")
page = st.sidebar.radio(
    "Navigazione",
    ["📊 Stats 8a.nu", "⛰️ Diario Vie Lunghe", "🧱 Cantiere Progetti"],
)

# -----------------------------------------------------------------------------
# PAGINA 1: STATISTICHE 8A.NU
# -----------------------------------------------------------------------------
if page == "📊 Stats 8a.nu":
  st.title("📊 Statistiche Falesia & Boulder (da 8a.nu)")

  ascents_data = load_json(ASCENTS_FILE)

  if not ascents_data:
    st.warning(
        "Nessun dato trovato in `data/ascents.json`. Esegui lo script"
        " `sync_8anu.py` per scaricare le ascensioni."
    )
  else:
    df = pd.DataFrame(ascents_data)

    # Filtri rapidi
    col1, col2, col3 = st.columns(3)
    col1.metric("Totale Ascensioni", len(df))
    col2.metric("Falesie Visitate", df["cragName"].nunique())
    col3.metric("Grado Max", df["difficulty"].max() if "difficulty" in df else "N/D")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
      st.subheader("Piramide dei Gradi")
      grade_counts = (
          df["difficulty"].value_counts().reset_index()
      )
      grade_counts.columns = ["Grado", "Numero"]
      fig_grades = px.bar(
          grade_counts,
          x="Grado",
          y="Numero",
          color="Numero",
          color_continuous_scale="Viridis",
      )
      st.plotly_chart(fig_grades, use_container_width=True)

    with col_right:
      st.subheader("Stile di Salita")
      if "flag" in df:
        style_counts = df["flag"].value_counts().reset_index()
        style_counts.columns = ["Stile", "Conteggio"]
        fig_style = px.pie(
            style_counts,
            names="Stile",
            values="Conteggio",
            hole=0.4,
        )
        st.plotly_chart(fig_style, use_container_width=True)

    st.subheader("📋 Registro Ascensioni")
    st.dataframe(
        df[["date", "routeName", "cragName", "difficulty", "flag", "comment"]],
        use_container_width=True,
    )

# -----------------------------------------------------------------------------
# PAGINA 2: DIARIO VIE LUNGHE
# -----------------------------------------------------------------------------
elif page == "⛰️ Diario Vie Lunghe":
  st.title("⛰️ Registro Vie Lunghe")

  vie = load_json(VIE_LUNGHE_FILE)

  with st.expander("➕ Aggiungi Nuova Via Lunga"):
    with st.form("form_via_lunga"):
      col_a, col_b = st.columns(2)
      nome = col_a.text_input("Nome Via")
      gruppo = col_b.text_input("Gruppo Montuoso / Cima")
      grado_max = col_a.text_input("Grado Max (es. 7a)")
      grado_obb = col_b.text_input("Grado Obbligatorio (es. 6b)")
      sviluppo = col_a.number_input("Sviluppo (metri)", min_value=0, step=10)
      tiri = col_b.number_input("Numero Tiri", min_value=1, step=1)
      compagno = col_a.text_input("Compagno/i di cordata")
      data = col_b.date_input("Data Ascensioni")
      note = st.text_area("Diario e Note Tattiche/Relazione")

      submitted = st.form_submit_button("Salva Via Lunga")
      if submitted and nome:
        nuova_via = {
            "nome": nome,
            "gruppo": gruppo,
            "grado_max": grado_max,
            "grado_obb": grado_obb,
            "sviluppo": sviluppo,
            "tiri": tiri,
            "compagno": compagno,
            "data": str(data),
            "note": note,
        }
        vie.append(nuova_via)
        save_json(VIE_LUNGHE_FILE, vie)
        st.success(f"Via '{nome}' salvata con successo!")
        st.rerun()

  if vie:
    df_vie = pd.DataFrame(vie)
    st.dataframe(df_vie, use_container_width=True)
  else:
    st.info("Nessuna via lunga registrata finora.")

# -----------------------------------------------------------------------------
# PAGINA 3: CANTIERE PROGETTI
# -----------------------------------------------------------------------------
elif page == "🧱 Cantiere Progetti":
  st.title("🧱 Progetti in Falesia")

  progetti = load_json(PROGETTI_FILE)

  with st.expander("➕ Nuovo Progetto in Cantiere"):
    with st.form("form_progetto"):
      falesia = st.text_input("Falesia / Settore")
      nome_progetto = st.text_input("Nome della Via")
      grado_stimato = st.text_input("Grado Stimato")
      stato = st.selectbox(
          "Stato", ["In prova", "Vicino alla catena", "Chiuso 🟢"]
      )
      metodo = st.text_area("Beta / Sequenze e Metodi")
      tentativi = st.number_input("Numero Tentativi Totali", min_value=1, step=1)

      submitted_p = st.form_submit_button("Salva Progetto")
      if submitted_p and nome_progetto:
        nuovo_progetto = {
            "falesia": falesia,
            "nome": nome_progetto,
            "grado": grado_stimato,
            "stato": stato,
            "tentativi": tentativi,
            "beta": metodo,
        }
        progetti.append(nuovo_progetto)
        save_json(PROGETTI_FILE, progetti)
        st.success(f"Progetto '{nome_progetto}' aggiornato!")
        st.rerun()

  if progetti:
    for i, p in enumerate(progetti):
      with st.container():
        st.subheader(f"{p['nome']} ({p['grado']}) - {p['falesia']}")
        st.caption(
            f"Stato: **{p['stato']}** | Tentativi: **{p['tentativi']}**"
        )
        st.write(f"**Metodi / Beta:** {p['beta']}")
        st.markdown("---")
  else:
    st.info("Nessun progetto attivo al momento.")
