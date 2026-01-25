import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client, Client

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Magazyn w Chmurze", page_icon="☁️", layout="wide")

# --- POŁĄCZENIE Z SUPABASE ---
# Używamy st.cache_resource, aby nie łączyć się przy każdym kliknięciu
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

# --- POBIERANIE DANYCH ---
def get_data():
    response = supabase.table("inventory").select("*").execute()
    data = response.data
    
    if not data:
        return pd.DataFrame() # Zwróć pustą ramkę, jeśli brak danych
        
    df = pd.DataFrame(data)
    
    # Obliczenia dodatkowe
    df['total_value'] = df['quantity'] * df['price']
    df['status'] = df.apply(lambda x: '⚠️ Krytyczny' if x['quantity'] <= x['min_stock'] else '✅ OK', axis=1)
    return df

# --- DODAWANIE DANYCH (CRUD) ---
def add_item(product, category, qty, min_qty, price):
    new_data = {
        "product": product,
        "category": category,
        "quantity": qty,
        "min_stock": min_qty,
        "price": price
    }
    supabase.table("inventory").insert(new_data).execute()

# --- INTERFEJS ---
st.title("☁️ Dashboard Magazynowy (Live DB)")

# Pobranie danych
df = get_data()

if df.empty:
    st.warning("Baza danych jest pusta. Dodaj pierwszy towar w panelu bocznym!")
else:
    # 1. KPI
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Ilość sztuk", df['quantity'].sum())
    col2.metric("💰 Wartość magazynu", f"{df['total_value'].sum():.2f} PLN")
    krytyczne = len(df[df['status'] == '⚠️ Krytyczny'])
    col3.metric("🚨 Alerty", krytyczne, delta_color="inverse")

    st.markdown("---")

    # 2. WYKRESY
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Ilość vs Minimum")
        fig = px.bar(df, x='product', y='quantity', color='status', 
                     color_discrete_map={'✅ OK': '#00CC96', '⚠️ Krytyczny': '#EF553B'},
                     hover_data=['min_stock'])
        # Dodanie linii granicznej (opcjonalne, uproszczone)
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.subheader("Wartość w kategoriach")
        fig2 = px.pie(df, values='total_value', names='category', hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)

    # 3. TABELA DANYCH
    st.subheader("📋 Szczegółowa lista")
    st.dataframe(df[['product', 'category
