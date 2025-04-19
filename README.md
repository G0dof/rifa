# 🎟️  RIFA — Aplicação Web com Streamlit

## 📌 Descrição

Este projeto é uma aplicação web interativa para rifas de 100 números, desenvolvida com Python utilizando as bibliotecas **Streamlit** e **Pandas**.

Agora com suporte a:

- ✅ Login e cadastro de usuários  
- 🔐 Rifas separadas para cada usuário  
- ✅ Reservar números com seu nome  
- 🎯 Realizar um sorteio aleatório  
- 📋 Visualizar os números escolhidos em tempo real

---

## 📦 Dependências

- streamlit  
- pandas  
- bcrypt

Instale com:

> pip install -r requirements.txt

---

## 🚀 Como Rodar

1. Clone ou baixe este repositório  
2. No terminal, navegue até a pasta do projeto  
3. Execute o comando:

> streamlit run main.py


A aplicação será aberta automaticamente no navegador (geralmente em [http://localhost:8501](http://localhost:8501))

---

## 📁 Funcionalidade de Login

- Na primeira tela, você pode se cadastrar como novo usuário  
- Após o login, sua rifa pessoal será carregada  
- Cada usuário tem sua própria tabela de reserva e sorteio  
- Os dados são armazenados em arquivos separados dentro da pasta `/rifas`

---

## 🧩 Segurança

- As senhas são criptografadas com `bcrypt`  
- O login é simples, local e persistente em `users.json`  
- Ideal para uso individual ou compartilhado com segurança básica

---

## 👤 Autor

Desenvolvido por **@G0dof**  
GitHub: [https://github.com/G0dof/rifa](https://github.com/G0dof/rifa)
