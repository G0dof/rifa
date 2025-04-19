import streamlit as st
import pandas as pd
import os
import json
import bcrypt

# Config
st.set_page_config(page_title="Rifa 10x10")
TOTAL_COLUMNS = 10
TOTAL_ROWS = 10
TOTAL_NUMBERS = TOTAL_COLUMNS * TOTAL_ROWS
DATA_FOLDER = "rifas"
USERS_FILE = "users.json"

# Criar pasta de rifas se não existir
os.makedirs(DATA_FOLDER, exist_ok=True)

# Funções de autenticação
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users_dict):
    with open(USERS_FILE, "w") as f:
        json.dump(users_dict, f)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Session init
if "users" not in st.session_state:
    st.session_state.users = load_users()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Página de Login e Cadastro
def login_page():
    st.title("🔐 Login / Cadastro")
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Cadastro"])

    with tab1:
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            users = st.session_state.users
            if username in users and verify_password(password, users[username]):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Bem-vindo, {username}!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    with tab2:
        new_user = st.text_input("Novo usuário")
        new_pass = st.text_input("Nova senha", type="password")
        if st.button("Cadastrar"):
            if new_user in st.session_state.users:
                st.warning("Este usuário já existe.")
            elif new_user and new_pass:
                hashed = hash_password(new_pass)
                st.session_state.users[new_user] = hashed
                save_users(st.session_state.users)
                st.success("Usuário cadastrado com sucesso! Faça login.")
            else:
                st.error("Preencha todos os campos.")

# Funções de dados por usuário
def user_filename(username):
    return os.path.join(DATA_FOLDER, f"{username}.csv")

def load_user_data(username):
    filename = user_filename(username)
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        if "winner_number" not in df.columns:
            df["winner_number"] = None
            df["winner_name"] = None
            df.to_csv(filename, index=False)
    else:
        df = pd.DataFrame({
            "number": list(range(1, TOTAL_NUMBERS + 1)),
            "name": [None] * TOTAL_NUMBERS,
            "winner_number": [None] * TOTAL_NUMBERS,
            "winner_name": [None] * TOTAL_NUMBERS
        })
        df.to_csv(filename, index=False)
    return df

def save_user_data(username, df):
    df.to_csv(user_filename(username), index=False)

# Proteção por login
if not st.session_state.logged_in:
    login_page()
    st.stop()

username = st.session_state.username
df = load_user_data(username)

# Sidebar - logout
with st.sidebar:
    st.caption(f"👤 Logado como: `{username}`")
    if st.button("🚪 Sair"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# Tabs
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

            if cols[j].button(label, key=f"btn_{username}_{idx}"):
                if not name:
                    st.warning("Digite um nome para marcar ou desmarcar o número.")
                elif pd.isna(current_name):
                    df.at[idx, "name"] = name
                    st.success(f"Número {num} reservado por {name}.")
                else:
                    df.at[idx, "name"] = None
                    st.info(f"Número {num} foi liberado.")
                save_user_data(username, df)
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
                save_user_data(username, df)
                st.rerun()
            else:
                st.warning("Nenhum número foi escolhido ainda para sortear.")
