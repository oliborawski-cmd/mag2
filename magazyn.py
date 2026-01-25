
import streamlit as st
import os

# --- Konfiguracja Strony ---
st.set_page_config(
    layout="wide", 
    page_title="📦 Magazyn GitHub Ready",
    initial_sidebar_state="collapsed"
)

DB_FILE = "inventory_db.txt"

# --- Funkcje Obsługi Pliku (Baza Danych) ---

def load_data():
    """Wczytuje dane z pliku tekstowego przy starcie."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            # Usuwamy puste linie i białe znaki
            return [line.strip() for line in f.readlines() if line.strip()]
    return ["🔨 Młotek", "🪛 Wkrętarka", "🔩 Śruby M8"]

def save_data():
    """Zapisuje aktualny stan magazynu do pliku."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        for item in st.session_state['inventory']:
            f.write(f"{item}\n")

# --- Inicjalizacja Stanu Sesji ---
if 'inventory' not in st.session_state:
    st.session_state['inventory'] = load_data()

# --- Logika Magazynu ---

def add_item():
    name = st.session_state.new_item_input.strip()
    if name:
        full_name = f"📦 {name}"
        if full_name not in st.session_state['inventory']:
            st.session_state['inventory'].append(full_name)
            save_data()  # Zapisujemy do pliku
            st.toast(f"Dodano: {name}", icon="✅")
        else:
            st.warning("Produkt już istnieje!")
        st.session_state.new_item_input = "" # Czyszczenie pola

def remove_item(item):
    st.session_state['inventory'].remove(item)
    save_data()  # Zapisujemy po usunięciu
    st.toast(f"Usunięto: {item}", icon="🗑️")

# --- Interfejs (UI) ---

st.title("🌟 Magazyn w Chmurze")
st.info("Dane są automatycznie zapisywane w pliku `inventory_db.txt` na serwerze.")

# Statystyki i Szukajka
inventory = st.session_state['inventory']
c1, c2 = st.columns([2, 1])
c1.metric("Suma towarów", len(inventory))
search = c2.text_input("🔍 Filtruj listę...", placeholder="Szukaj...")

st.divider()

# Dodawanie
with st.container():
    col1, col2 = st.columns([4, 1])
    col1.text_input("Nazwa towaru:", key="new_item_input", on_change=add_item, placeholder="Wpisz nazwę i naciśnij Enter...")
    if col2.button("➕ DODAJ", type="primary", use_container_width=True):
        add_item()

st.write("##")

# Wyświetlanie listy
filtered_items = [i for i in inventory if search.lower() in i.lower()]

if filtered_items:
    for idx, item in enumerate(filtered_items):
        row_col1, row_col2, row_col3 = st.columns([0.5, 4.5, 1])
        row_col1.write(f"#{idx+1}")
        row_col2.subheader(item)
        if row_col3.button("Usuń", key=f"del_{item}", use_container_width=True):
            remove_item(item)
            st.rerun()
else:
    st.write("Brak towarów w magazynie.")
