import streamlit as st

# --- Konfiguracja Strony i Tytuł ---
st.set_page_config(
    layout="wide", 
    page_title="📦 Wizualny Magazyn",
    initial_sidebar_state="collapsed"
)

# --- Inicjalizacja Danych (Stan) ---

if 'inventory_container' not in st.session_state:
    st.session_state['inventory_container'] = st.empty()
    # Dodano emotikony do początkowych danych
    st.session_state['inventory'] = ["🔨 Młotek", "🪛 Wkrętarka", "🔩 Śruby M8"] 

# Pobieranie aktualnej listy towarów
inventory = st.session_state['inventory']

# --- Funkcje Logiki Magazynu ---

def add_item(item_name):
    """Dodaje towar do listy, jeśli pole nie jest puste."""
    if item_name:
        # Dodajemy ikonę paczki do nowo dodawanego elementu
        formatted_item = f"📦 {item_name.strip()}"
        inventory.append(formatted_item)
        st.session_state['inventory'] = inventory
        st.success(f"✅ Dodano towar: **{item_name}**")
    else:
        st.warning("⚠️ Nazwa towaru nie może być pusta.")

def remove_item(item_name):
    """Usuwa towar z listy."""
    try:
        inventory.remove(item_name)
        st.session_state['inventory'] = inventory
        # Użycie st.error (czerwony) jako mocniejszy kolor usuwania
        st.error(f"🗑️ Usunięto towar: **{item_name.replace('📦 ', '')}**") 
    except ValueError:
        st.error(f"❌ Błąd: Towar **{item_name.replace('📦 ', '')}** nie znajduje się na liście.")

# --- Interfejs Użytkownika Streamlit ---

st.title("🌟 Wizualny Magazyn Narzędzi")
st.caption("Stan magazynu utrzymywany dynamicznie w pamięci aplikacji.")

# --- Wizualizacja Stanu Magazynu (Panel informacyjny) ---

col_info_1, col_info_2 = st.columns(2)

col_info_1.info(f"🔢 Aktualna liczba unikalnych towarów: **{len(inventory)}**")

if len(inventory) > 5:
    col_info_2.success("✨ Magazyn dobrze zaopatrzony! Kontynuuj dobrą pracę.")
else:
    col_info_2.warning("⏳ Magazyn wymaga uzupełnienia. Dodaj więcej towarów.")

st.divider()

# --- Panel Dodawania Towaru (Użycie Koloru Głównego) ---

with st.expander("➕ Dodaj Nowy Towar", expanded=True):
    col1, col2 = st.columns([3, 1])
    
    new_item_name = col1.text_input(
        "Nazwa Towaru:", 
        key="new_item_input", 
        label_visibility="collapsed", 
        placeholder="Wpisz nazwę towaru (np. 'Klucz płaski')..."
    )
    
    # Przycisk w kolorze "primary" (domyślny niebieski/zielony)
    col2.button(
        "➡️ DODAJ", 
        on_click=add_item, 
        args=(new_item_name,), 
        type="primary",
        use_container_width=True
    )

st.divider()

# --- Lista Magazynowa i Usuwanie (Kolorowe Wiersze) ---

st.header("📋 Aktualny Stan Magazynu")

if inventory:
    # Nagłówki kolumn
    col_index_head, col_item_head, col_btn_head = st.columns([0.5, 4.5, 1])
    col_item_head.subheader("Towar")
    col_btn_head.subheader("Akcja")
    
    st.markdown("---")

    # Tworzenie dynamicznej listy towarów z przyciskami do usuwania
    for i, item in enumerate(inventory):
        col_index, col_item, col_btn = st.columns([0.5, 4.5, 1])
        
        # Użycie kolorowego kontenera dla lepszej wizualizacji wiersza
        with col_item:
            st.markdown(f"### {item}") # Większy tekst dla towaru
        
        col_index.metric(label="#", value=i+1, delta_color="off")
        
        # Przycisk usuwania w kolorze "secondary" (szary/czerwony)
        col_btn.button(
            "✖️ Usuń", 
            key=f"remove_btn_{i}", 
            on_click=remove_item, 
            args=(item,),
            type="secondary",
            use_container_width=True
        )
    
    st.markdown("---")

else:
    st.error("🚨 Magazyn jest PUSTY! Proszę dodać towar, aby rozpocząć pracę.")

# Użycie ukrytego kontenera, aby Streamlit "pamiętał" listę
st.session_state['inventory_container'].empty()
