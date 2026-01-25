import streamlit as st
import pandas as pd
import os
import json

# --- Konfiguracja ---
st.set_page_config(layout="wide", page_title="📦 Magazyn Finansowy PRO")

DB_FILE = "inventory_data.json"

# --- Zarządzanie Danymi ---
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return [
        {"nazwa": "Młotek", "ilosc": 5, "cena": 45.0},
        {"nazwa": "Wkrętarka", "ilosc": 2, "cena": 350.0}
    ]

def save_data():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state['inventory'], f, indent=4, ensure_ascii=False)

if 'inventory' not in st.session_state:
    st.session_state['inventory'] = load_data()

# --- Funkcje Logiki ---
def add_item(name, qty, price):
    if name:
        new_item = {"nazwa": name, "ilosc": qty, "cena": price}
        st.session_state['inventory'].append(new_item)
        save_data()
        st.toast(f"Dodano {name}", icon="✅")
    else:
        st.error("Nazwa nie może być pusta!")

def remove_item(index):
    del st.session_state['inventory'][index]
    save_data()
    st.rerun()

# --- Interfejs Użytkownika (Dashboard) ---
st.title("📊 Magazyn z Analizą Kosztów")

# Obliczenia
inv = st.session_state['inventory']
total_items = sum(item['ilosc'] for item in inv)
total_value = sum(item['ilosc'] * item['cena'] for item in inv)
avg_price = total_value / len(inv) if inv else 0

# --- Panel Statystyk ---
col_s1, col_s2, col_s3 = st.columns(3)
col_s1.metric("Suma sztuk", f"{total_items} szt.")
col_s2.metric("Wartość magazynu", f"{total_value:,.2f} PLN")
col_s3.metric("Średnia wartość produktu", f"{avg_price:,.2f} PLN")

st.divider()

# --- Formularz Dodawania ---
with st.expander("➕ Dodaj nowy towar do bazy", expanded=True):
    with st.form("add_form", clear_on_submit=True):
        c1, c2, c3 = st.columns([3, 1, 1])
        name = c1.text_input("Nazwa przedmiotu", placeholder="Np. Kabel miedziany")
        qty = c2.number_input("Ilość", min_value=1, value=1)
        price = c3.number_input("Cena za szt. (PLN)", min_value=0.0, value=0.0, step=0.5)
        
        if st.form_submit_button("DODAJ DO EWIDENCJI", use_container_width=True):
            add_item(name, qty, price)
            st.rerun()

st.write("##")

# --- Tabela i Zarządzanie ---
st.header("📋 Wykaz Towarów")

if inv:
    # Nagłówki
    h1, h2, h3, h4, h5 = st.columns([3, 1, 1, 1, 1])
    h1.write("**Produkt**")
    h2.write("**Ilość**")
    h3.write("**Cena j.**")
    h4.write("**Wartość**")
    h5.write("**Akcja**")
    st.markdown("---")

    for idx, item in enumerate(inv):
        c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 1])
        c1.markdown(f"**{item['nazwa']}**")
        c2.write(f"{item['ilosc']} szt.")
        c3.write(f"{item['cena']:.2f} PLN")
        
        wartosc = item['ilosc'] * item['cena']
        c4.write(f"**{wartosc:.2f} PLN**")
        
        if c5.button("Usuń", key=f"del_{idx}", type="secondary", use_container_width=True):
            remove_item(idx)
else:
    st.info("Brak towarów. Użyj powyższego formularza, aby zasilić magazyn.")
    
