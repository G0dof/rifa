import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Rifa 10x10")

FILENAME = "rifa.csv"
TOTAL_COLUMNS = 10
TOTAL_ROWS = 10
TOTAL_NUMBERS = TOTAL_COLUMNS * TOTAL_ROWS

def load_data():
    if os.path.exists(FILENAME):
        df = pd.read_csv(FILENAME)
        if "winner_number" not in df.columns:
            df["winner_number"] = None
            df["winner_name"] = None
            df.to_csv(FILENAME, index=False)
    else:
        df = pd.DataFrame({
            "number": list(range(1, TOTAL_NUMBERS + 1)),
            "name": [None] * TOTAL_NUMBERS,
            "winner_number": [None] * TOTAL_NUMBERS,
            "winner_name": [None] * TOTAL_NUMBERS
        })
        df.to_csv(FILENAME, index=False)
    return df

def save_data(df):
    df.to_csv(FILENAME, index=False)

df = load_data()

tab1, tab2 = st.tabs(["📋 Tabela de Rifa", "🎲 Sorteio"])

with tab1:
    st.title("📋 Tabela de Rifa")
    name = st.text_input("✍️ Digite um nome para marcar ou desmarcar um número:")

    cols = st.columns(TOTAL_COLUMNS)
    for i in range(TOTAL_ROWS):
        for j in range(TOTAL_COLUMNS):
            idx = i * TOTAL_COLUMNS + j
            num = df.at[idx, "number"]
            current_name = df.at[idx, "name"]
            label = f"✅ {num:02d}" if pd.notna(current_name) else f"⬜ {num:02d}"

            if cols[j].button(label, key=f"btn_{idx}"):
                if not name:
                    st.warning("Digite um nome para marcar ou desmarcar o número.")
                elif pd.isna(current_name):
                    df.at[idx, "name"] = name
                    st.success(f"Número {num} reservado por {name}.")
                else:
                    df.at[idx, "name"] = None
                    st.info(f"Número {num} foi liberado.")
                save_data(df)
                st.rerun()

    with st.sidebar:
        st.header("📋 Números Escolhidos")
        chosen = df[df["name"].notna()]
        if not chosen.empty:
            for _, row in chosen.iterrows():
                st.write(f"🔢 {int(row['number']):02d}: {row['name']}")
        else:
            st.info("Nenhum número foi escolhido ainda.")

with tab2:
    st.title("🎲 Sorteio da Rifa")
    winner_row = df[df["winner_name"].notna()]

    if not winner_row.empty:
        winner_num = int(winner_row.iloc[0]["winner_number"])
        winner_name = winner_row.iloc[0]["winner_name"]
        st.success(f"🏆 Número sorteado: **{winner_num:02d}** — {winner_name}")
    else:
        if st.button("Sortear um Ganhador"):
            chosen = df[df["name"].notna()]
            if not chosen.empty:
                picked = chosen.sample(1).iloc[0]
                winner_num = int(picked["number"])
                winner_name = picked["name"]
                st.success(f"🏆 Número sorteado: **{winner_num:02d}** — {winner_name}")
                df.at[0, "winner_number"] = winner_num
                df.at[0, "winner_name"] = winner_name
                save_data(df)
                st.rerun()
            else:
                st.warning("Nenhum número foi escolhido ainda para sortear.")
