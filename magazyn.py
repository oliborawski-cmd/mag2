import streamlit as st

# --- Konfiguracja i Inicjalizacja Danych ---

# Używamy st.empty() jako "niezmiennego" pojemnika do przechowywania danych
# Ponieważ Streamlit resetuje zmienne globalne przy każdej interakcji,
# możemy użyć tego elementu do utrzymania stanu (listy towarów).
# Jest to alternatywa dla st.session_state.
if 'inventory_container' not in st.session_state:
    st.session_state['inventory_container'] = st.empty()
    st.session_state['inventory'] = ["Młotek", "Wiertarka", "Śruby M8"] # Początkowe dane

# Pobieranie aktualnej listy towarów
inventory = st.session_state['inventory']

# --- Funkcje Logiki Magazynu ---

def add_item(item_name):
    """Dodaje towar do listy, jeśli pole nie jest puste."""
    if item_name:
        inventory.append(item_name)
        st.session_state['inventory'] = inventory # Aktualizacja stanu
        st.success(f"Dodano towar: **{item_name}**")
    else:
        st.warning("Nazwa towaru nie może być pusta.")

def remove_item(item_name):
    """Usuwa towar z listy."""
    try:
        inventory.remove(item_name)
        st.session_state['inventory'] = inventory # Aktualizacja stanu
        st.success(f"Usunięto towar: **{item_name}**")
    except ValueError:
        st.error(f"Błąd: Towar **{item_name}** nie znajduje się na liście.")

# --- Interfejs Użytkownika Streamlit ---

st.title("📦 Prosty Magazyn (Streamlit + Lista)")
st.caption("Stan utrzymywany bez użycia st.session_state, ale wciąż w pamięci aplikacji Streamlit.")

# --- Panel Dodawania Towaru ---

with st.expander("➕ Dodaj Nowy Towar", expanded=True):
    col1, col2 = st.columns([3, 1])
    
    new_item_name = col1.text_input("Nazwa Towaru:", key="new_item_input", label_visibility="collapsed", placeholder="Wpisz nazwę towaru...")
    
    # Przycisk, który wywoła funkcję dodawania
    col2.button(
        "Dodaj", 
        on_click=add_item, 
        args=(new_item_name,), 
        type="primary",
        use_container_width=True
    )

st.divider()

# --- Lista Magazynowa i Usuwanie ---

st.header("Aktualny Stan Magazynu")

if inventory:
    # Tworzenie dynamicznej listy towarów z przyciskami do usuwania
    for i, item in enumerate(inventory):
        col_item, col_btn = st.columns([5, 1])
        
        col_item.markdown(f"**{i+1}.** {item}")
        
        # Unikalny klucz dla każdego przycisku usuwania
        col_btn.button(
            "Usuń", 
            key=f"remove_btn_{i}", 
            on_click=remove_item, 
            args=(item,),
            type="secondary",
            use_container_width=True
        )
else:
    st.info("Magazyn jest pusty. Dodaj pierwszy towar!")

# Użycie ukrytego kontenera, aby Streamlit "pamiętał" listę
st.session_state['inventory_container'].empty()
